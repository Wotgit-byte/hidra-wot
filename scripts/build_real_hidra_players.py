import openpyxl
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
EXCEL_PATH = os.path.join(ROOT_DIR, 'maniobras_sheet.xlsx')

wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
ws_rd = wb['Registro diario']

# Extract real player points and positions (Day 5 / latest)
real_hidra_players = {}
for r in range(5, ws_rd.max_row + 1):
    fecha = ws_rd.cell(row=r, column=2).value
    dia = ws_rd.cell(row=r, column=3).value
    jugador = ws_rd.cell(row=r, column=4).value
    puesto = ws_rd.cell(row=r, column=6).value
    puntos = ws_rd.cell(row=r, column=7).value
    equipo = ws_rd.cell(row=r, column=5).value
    
    if jugador and puntos is not None:
        pname = str(jugador).strip()
        if pname not in real_hidra_players or (dia and dia > real_hidra_players[pname]['dia']):
            real_hidra_players[pname] = {
                'name': pname,
                'dia': dia,
                'pos': int(puesto) if puesto else 9999,
                'pts': int(puntos),
                'team': str(equipo)
            }

# Load replay telemetry
telemetry_path = os.path.join(BASE_DIR, 'player_replay_stats.json')
telemetry = {}
if os.path.exists(telemetry_path):
    with open(telemetry_path, 'r', encoding='utf-8') as f:
        telemetry = json.load(f)

# Load WG members for role and official name
rosters_path = os.path.join(BASE_DIR, 'wg_rosters.json')
hidra_members = {}
if os.path.exists(rosters_path):
    with open(rosters_path, 'r', encoding='utf-8') as f:
        all_rosters = json.load(f)
        for m in all_rosters.get('[HIDRA]', {}).get('members', []):
            hidra_members[m.get('account_name', '').lower()] = m

CUTOFF_TOP_1000 = 3421 # Dia 5 official cutoff for top 1000

final_hidra_list = []
# Sort by points descending
sorted_by_pts = sorted(real_hidra_players.values(), key=lambda x: x['pts'], reverse=True)

for p in sorted_by_pts:
    pname = p['name']
    pts = p['pts']
    pos = p['pos']
    in_tank = (pos <= 1000) or (pts >= CUTOFF_TOP_1000)
    diff = pts - CUTOFF_TOP_1000
    
    # Telemetry from replays if available
    tel = telemetry.get(pname, {})
    dmg = tel.get('avg_dmg', 0)
    battles = tel.get('battles', 0)
    frags = f"{tel.get('avg_frags', 0.0):.2f}" if tel else "—"
    winrate = f"{tel.get('surv_rate', '—')}" # or estimate
    
    # Member role
    m_info = hidra_members.get(pname.lower(), {})
    role = m_info.get('role_i18n', m_info.get('role', 'Soldado'))
    
    prize = "750 Bonos" if in_tank else "250 Bonos"
    
    final_hidra_list.append({
        'pos': pos,
        'name': f"{pname} [HIDRA]",
        'role': role,
        'pts': pts,
        'diff': diff,
        'in_tank': in_tank,
        'damage': dmg,
        'battles': battles,
        'wins': "67.1%", # clan overall
        'frags': frags,
        'prize': prize,
        'fav_tank': tel.get('fav_tank', '—')
    })

print(f"Compiled {len(final_hidra_list)} official HIDRA players from Sheets!")
print(f"Players in tank: {sum(1 for p in final_hidra_list if p['in_tank'])}")

with open(os.path.join(BASE_DIR, 'hidra_real_players.json'), 'w', encoding='utf-8') as f:
    json.dump(final_hidra_list, f, indent=2, ensure_ascii=False)
