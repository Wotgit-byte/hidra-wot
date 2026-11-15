import openpyxl
import json

wb = openpyxl.load_workbook('maniobras_sheet_new.xlsx', data_only=True)
ws_p = wb['Registro Partidas']

with open('scripts/battles_data.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

excel_rows = []
for r in range(5, ws_p.max_row + 1):
    pid = ws_p.cell(row=r, column=2).value
    fecha = ws_p.cell(row=r, column=3).value
    mapa = ws_p.cell(row=r, column=5).value
    rival = ws_p.cell(row=r, column=6).value
    resultado = ws_p.cell(row=r, column=7).value
    marcador = ws_p.cell(row=r, column=11).value
    if pid and rival and marcador:
        dt_str = fecha.strftime('%m/%d/%Y') if hasattr(fecha, 'strftime') else str(fecha)[:10]
        map_clean = str(mapa).split('(')[0].strip() if mapa else ''
        res_clean = 'Victory' if str(resultado).strip().upper() == 'VICTORIA' else 'Defeat'
        score_clean = str(marcador).strip().replace('-', ':')
        clean_tag = str(rival).strip().strip('[]')
        excel_rows.append({
            'date': dt_str,
            'map': map_clean,
            'enemy': f"[{clean_tag}]",
            'result': res_clean,
            'score': score_clean
        })

print(f"Total excel rows with score: {len(excel_rows)}")

matched = 0
for er in excel_rows:
    for mb in master:
        if not mb.get('score'):
            if mb.get('date') == er['date'] and mb.get('enemy') == er['enemy']:
                if er['map'].lower() in mb.get('map', '').lower() and er['result'] == mb.get('result'):
                    mb['score'] = er['score']
                    matched += 1
                    break

print(f"Matched {matched} more battles with score!")
print(f"Total master with score now: {sum(1 for b in master if b.get('score'))}")
with open('scripts/battles_data.json', 'w', encoding='utf-8') as f:
    json.dump(master, f, indent=2, ensure_ascii=False)
