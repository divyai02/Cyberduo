from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')
client = MongoClient(os.getenv('MONGO_URI'))
db = client['cyberduo']
col = db['questions']

categories = ['phishing', 'password', 'malware', 'firewall', 'scams']
for cat in categories:
    query = {'game_key': cat, 'level_name': 'medium'}
    questions = list(col.find(query).sort('local_id', 1))
    print(f"Category: {cat}, Count: {len(questions)}")
    for q in questions[:5]: # Just check first 5
        print(f"  ID: {q['local_id']}, Concept: {q.get('concept', 'N/A')}")

client.close()
