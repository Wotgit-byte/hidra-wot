import json

with open('scripts/battles_data.json', 'r', encoding='utf-8') as f:
    battles = json.load(f)

reassigned_to_zotz = 0
reassigned_to_kavron = 0

for b in battles:
    d = b.get('date')
    c = b.get('commander')
    
    # 1. Ayer (11/14/2026): mario__invader -> zotz
    if d == '11/14/2026' and c == 'mario__invader':
        b['commander'] = 'zotz'
        reassigned_to_zotz += 1
        
    # 2. Antes de ayer (11/13/2026): zotz -> K4VR0N
    elif d == '11/13/2026' and c == 'zotz':
        b['commander'] = 'K4VR0N'
        reassigned_to_kavron += 1

print(f"Reasignadas a zotz (14/11): {reassigned_to_zotz}")
print(f"Reasignadas a K4VR0N (13/11): {reassigned_to_kavron}")

with open('scripts/battles_data.json', 'w', encoding='utf-8') as f:
    json.dump(battles, f, indent=2, ensure_ascii=False)
print("Guardado scripts/battles_data.json correctamente.")
