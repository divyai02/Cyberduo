import json

filepath = r'frontend\src\data\GameQuestions.json'
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data['phishing']['beginner']:
    print(f"ID: {q['id']} | Format: {q['format']}")
    print(f"Q: {q.get('questionText', '')}")
    if q['format'] == 'cyber_snakes_ladders':
        print(f"Scenario: {q.get('scenario', '')}")
    print("-" * 40)
