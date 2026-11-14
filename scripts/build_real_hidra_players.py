import openpyxl
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
EXCEL_PATH = os.path.join(ROOT_DIR, 'maniobras_sheet.xlsx')

wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
ws_rd = wb['Registro diario']

# Day 5 official data
# Cutoff for tank is top 2.000 in NA (1,459 pts on Day 5)
CUTOFF_TOP_2000_PTS = 1459

def puntos_val(p):
    return p is not None and str(p).replace('.', '').isdigit()

day5_players = {}
for r in range(5, ws_rd.max_row + 1):
    dia = ws_rd.cell(row=r, column=3).value
    pname = ws_rd.cell(row=r, column=4).value
    pos = ws_rd.cell(row=r, column=6).value
    pts = ws_rd.cell(row=r, column=7).value
    equipo = ws_rd.cell(row=r, column=5).value
    
    if dia == 5 and pname and pos is not None and puntos_val(pts):
        pname_str = str(pname).strip()
        day5_players[pname_str] = {
            'name': pname_str,
            'pos': int(pos),
            'pts': int(pts),
            'team': str(equipo)
        }

# Load WG members for role and official name
rosters_path = os.path.join(BASE_DIR, 'wg_rosters.json')
hidra_members = {}
if os.path.exists(rosters_path):
    with open(rosters_path, 'r', encoding='utf-8') as f:
        all_rosters = json.load(f)
        for m in all_rosters.get('[HIDRA]', {}).get('members', []):
            hidra_members[m.get('account_name', '').lower()] = m

# Replay telemetry
telemetry_path = os.path.join(BASE_DIR, 'player_replay_stats.json')
telemetry = {}
if os.path.exists(telemetry_path):
    with open(telemetry_path, 'r', encoding='utf-8') as f:
        telemetry = json.load(f)

# Sort strictly by position in NA ascending (Rank #1 to #4000)
sorted_players = sorted(day5_players.values(), key=lambda x: x['pos'])

final_hidra_list = []
for p in sorted_players:
    pname = p['name']
    pos = p['pos']
    pts = p['pts']
    
    # Official rule: in tank if pos <= 2000
    in_tank = (pos <= 2000)
    diff = pts - CUTOFF_TOP_2000_PTS
    
    # Telemetry
    tel = telemetry.get(pname)
    if tel and tel.get('battles', 0) > 0:
        dmg_val = tel.get('avg_dmg', 0)
        dmg_str = f"{dmg_val:,}"
        battles_str = str(tel.get('battles', 0))
        frags_str = f"{tel.get('avg_frags', 0.0):.2f}"
        wins_str = f"{tel.get('surv_rate', '—')}"
    else:
        dmg_str = "—"
        battles_str = "—"
        frags_str = "—"
        wins_str = "—"
        
    m_info = hidra_members.get(pname.lower(), {})
    role = m_info.get('role_i18n', m_info.get('role', 'Soldado'))
    
    # Reward: 250 / 400 / 500 / 600 / 700 Bonos based on rank
    if pos <= 500:
        prize = "700 Bonos"
    elif pos <= 1000:
        prize = "600 Bonos"
    elif pos <= 1500:
        prize = "500 Bonos"
    elif pos <= 1900:
        prize = "400 Bonos"
    elif pos <= 2700:
        prize = "250 Bonos"
    else:
        prize = "Sin Bonos"

    final_hidra_list.append({
        'pos': pos,
        'name': f"{pname} [HIDRA]",
        'role': role,
        'pts': pts,
        'diff': diff,
        'in_tank': in_tank,
        'damage_str': dmg_str,
        'battles_str': battles_str,
        'wins_str': wins_str,
        'frags_str': frags_str,
        'prize': prize
    })

print(f"Total players processed: {len(final_hidra_list)}")
print(f"In tank (pos <= 2000): {sum(1 for p in final_hidra_list if p['in_tank'])}")
print(f"Out of tank (pos > 2000): {sum(1 for p in final_hidra_list if not p['in_tank'])}")

with open(os.path.join(BASE_DIR, 'hidra_real_players.json'), 'w', encoding='utf-8') as f:
    json.dump(final_hidra_list, f, indent=2, ensure_ascii=False)
