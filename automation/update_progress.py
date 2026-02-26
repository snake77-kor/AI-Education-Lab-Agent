import json

file_path = "/Users/byeongtaekkim/Documents/multi-AI agents/automation/infographic_progress.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

data["csat_vocabulary"]["current_day"] += 1
data["csat_grammar"]["current_point"] += 1
data["ms_grammar"]["current_point"] += 1

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Progress updated successfully.")
