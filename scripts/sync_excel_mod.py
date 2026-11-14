import openpyxl
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
EXCEL_PATH = os.path.join(ROOT_DIR, 'maniobras_sheet.xlsx')

wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)

# 1. Enrich master battles from 'Registro Partidas'
with open(os.path.join(BASE_DIR, 'battles_data.json'), 'r', encoding='utf-8') as f:
    master_battles = json.load(f)

ws_p = wb['Registro Partidas']
excel_battles = []
for r in range(5, ws_p.max_row + 1):
    pid = ws_p.cell(row=r, column=2).value
    fecha_val = ws_p.cell(row=r, column=3).value
    equipo = ws_p.cell(row=r, column=4).value
    mapa = ws_p.cell(row=r, column=5).value
    rival = ws_p.cell(row=r, column=6).value
    resultado = ws_p.cell(row=r, column=7).value
    marcador = ws_p.cell(row=r, column=11).value
    if pid and rival:
        dt_str = fecha_val.strftime('%m/%d/%Y') if hasattr(fecha_val, 'strftime') else str(fecha_val)[:10]
        map_clean = str(mapa).split('(')[0].strip() if mapa else ''
        res_clean = 'Victory' if str(resultado).strip().upper() == 'VICTORIA' else 'Defeat'
        score_clean = str(marcador).strip().replace('-', ':') if marcador else None
        excel_battles.append({
            'pid': str(pid),
            'date': dt_str,
            'team': equipo,
            'map': map_clean,
            'enemy': f"[{str(rival).strip().strip('[]')}]",
            'result': res_clean,
            'score': score_clean
        })

matched = 0
for eb in excel_battles:
    for mb in master_battles:
        if mb.get('date') == eb['date'] and mb.get('enemy') == eb['enemy'] and eb['map'].lower() in mb.get('map', '').lower():
            if mb.get('result') == eb['result']:
                if not mb.get('score') and eb.get('score'):
                    mb['score'] = eb['score']
                    matched += 1
                if not mb.get('pid'):
                    mb['pid'] = eb['pid']

print(f"Enriched {matched} master battles with score & pid from Excel.")
with open(os.path.join(BASE_DIR, 'battles_data.json'), 'w', encoding='utf-8') as f:
    json.dump(master_battles, f, indent=2, ensure_ascii=False)

# 2. Extract player telemetry from 'Detalle de aliados y enemigos'
ws_det = wb['Detalle de aliados y enemigos']
player_stats = {}
for r in range(5, ws_det.max_row + 1):
    lado = ws_det.cell(row=r, column=3).value
    if lado != 'ALIADO':
        continue
    tanque = ws_det.cell(row=r, column=4).value
    jugador = ws_det.cell(row=r, column=5).value
    dmg = ws_det.cell(row=r, column=7).value or 0
    frags = ws_det.cell(row=r, column=8).value or 0
    assist = ws_det.cell(row=r, column=9).value or 0
    estado = ws_det.cell(row=r, column=14).value
    
    if not jugador:
        continue
        
    pname = str(jugador).strip()
    if pname not in player_stats:
        player_stats[pname] = {
            'battles': 0, 'damage': 0, 'frags': 0, 'assist': 0, 'survived': 0, 'tanks': {}
        }
    
    ps = player_stats[pname]
    ps['battles'] += 1
    ps['damage'] += int(dmg)
    ps['frags'] += int(frags)
    ps['assist'] += int(assist)
    if estado == 'Vivo':
        ps['survived'] += 1
    
    tname = str(tanque).strip() if tanque else 'Desconocido'
    ps['tanks'][tname] = ps['tanks'].get(tname, 0) + 1

for p, s in player_stats.items():
    b = s['battles']
    s['avg_dmg'] = round(s['damage'] / b) if b > 0 else 0
    s['avg_assist'] = round(s['assist'] / b) if b > 0 else 0
    s['avg_frags'] = round(s['frags'] / b, 2) if b > 0 else 0.0
    s['surv_rate'] = f"{round((s['survived'] / b) * 100)}%" if b > 0 else '0%'
    if s['tanks']:
        top_t = max(s['tanks'].items(), key=lambda x: x[1])
        s['fav_tank'] = f"{top_t[0]} ({top_t[1]})"
    else:
        s['fav_tank'] = '—'

with open(os.path.join(BASE_DIR, 'player_replay_stats.json'), 'w', encoding='utf-8') as f:
    json.dump(player_stats, f, indent=2, ensure_ascii=False)
print(f"Extracted real telemetry for {len(player_stats)} HIDRA players.")
