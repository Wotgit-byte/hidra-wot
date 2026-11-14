import json
import re

with open(r'C:\Users\K4v16\.gemini\antigravity\brain\dae1f4ed-6509-4bce-a63f-960d8a2838eb\scratch\transcribe_new_batches.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Extract list
start = code.find("new_battles = [")
end = code.find("\nprint(f\"Total newly transcribed")
if end == -1:
    end = code.find("\nprint(")

sub_code = code[start:end]
globs = {}
exec(sub_code, globs)
new_battles = globs["new_battles"]
print(f"Extracted new_battles: {len(new_battles)}")

with open("scripts/battles_data.json", "r", encoding="utf-8") as f:
    master = json.load(f)

print(f"Master before: {len(master)}")

def is_in_window(b):
    t = b["time"].replace(" AM", "").replace(" PM", "").strip()
    parts = [int(x) for x in t.split(":")]
    total_m = parts[0] * 60 + parts[1]
    return 180 <= total_m <= 310

valid_new = [b for b in new_battles if is_in_window(b)]
print(f"Valid new battles in window 3:00-5:10 AM: {len(valid_new)}")

def battle_key(b):
    return (b.get("date"), b.get("time", "").strip(), b.get("enemy", "").strip(), b.get("map", "").strip())

master_keys = set(battle_key(b) for b in master)

added = 0
for b in valid_new:
    k = battle_key(b)
    if k not in master_keys:
        master.append(b)
        master_keys.add(k)
        added += 1

print(f"Added new battles: {added}")
print(f"Master total now: {len(master)}")

with open("scripts/battles_data.json", "w", encoding="utf-8") as f:
    json.dump(master, f, indent=2, ensure_ascii=False)
print("Successfully saved scripts/battles_data.json")
