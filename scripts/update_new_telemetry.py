import openpyxl
import json
import os

wb = openpyxl.load_workbook('maniobras_sheet_new.xlsx', data_only=True)
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
        player_stats[pname] = {'battles': 0, 'damage': 0, 'frags': 0, 'assist': 0, 'survived': 0, 'tanks': {}}
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

with open('scripts/player_replay_stats.json', 'w', encoding='utf-8') as f:
    json.dump(player_stats, f, indent=2, ensure_ascii=False)

print(f"Updated scripts/player_replay_stats.json with {len(player_stats)} players from new sheet!")
