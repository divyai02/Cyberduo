import json
import os

filepath = r'frontend\src\data\GameQuestions.json'
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

q_list = data['phishing']['beginner']
for q in q_list:
    # Fix quishing_drills missing options
    if q['format'] == 'quishing_drills' and 'options' not in q:
        q['options'] = ['Safe', 'Phishing']
    
    # Fix adversary_roleplay missing options if assets also missing
    if q['format'] == 'adversary_roleplay' and 'options' not in q and 'assets' not in q:
        q['options'] = ['Campaign A', 'Campaign B']
    
    # Ensure capture_the_flag objects have consistent format
    if q['format'] == 'capture_the_flag' or q['format'] == 'scavenger_hunt':
        if 'objects' in q:
            for obj in q['objects']:
                if 'isRedFlag' not in obj and 'isFlag' in obj:
                    obj['isRedFlag'] = obj['isFlag']

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("GameQuestions.json fixed successfully.")
