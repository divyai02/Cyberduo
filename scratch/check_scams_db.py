from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')
client = MongoClient(os.getenv('MONGO_URI'))
db = client['cyberduo']
col = db['questions']

query = {'game_key': 'scams', 'level_name': 'medium'}
questions = list(col.find(query).sort('local_id', 1))

print(f"Found {len(questions)} questions for scams medium")
for q in questions:
    print(f"ID: {q['local_id']}, Concept: {q.get('concept', 'N/A')}, Format: {q['format']}")

client.close()
