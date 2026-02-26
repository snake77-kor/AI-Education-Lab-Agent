import json

with open('/Users/byeongtaekkim/Documents/multi-AI agents/automation/infographic_progress.json', 'r') as f:
    data = json.load(f)

data['csat_vocabulary']['current_day'] += 1
data['csat_grammar']['current_point'] += 1
data['ms_grammar']['current_point'] += 1

with open('/Users/byeongtaekkim/Documents/multi-AI agents/automation/infographic_progress.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Progress JSON updated!")
