import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load env variables
load_dotenv('backend/.env')
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
client = MongoClient(mongo_uri)
db = client['cyberduo']
collection = db['questions']

# Fetch and update omni_threat_chains in mongo
queries = list(collection.find({'game_key': 'phishing', 'format': 'omni_threat_chains'}))
for q in queries:
    # Set correct answer to the part with isFlag: true
    correct_part = next((part['text'] for ch in q.get('channels', []) for part in ch.get('parts', []) if part.get('isFlag')), None)
    if correct_part:
        collection.update_one({'_id': q['_id']}, {'$set': {'correctAnswer': correct_part}})
        print(f"Updated Q{q['id']} with {correct_part}")

# Fetch and update capture_the_flag to show correct objects
queries = list(collection.find({'game_key': 'phishing', 'format': 'capture_the_flag'}))
for q in queries:
    correct_objs = [obj['label'] for obj in q.get('objects', []) if obj.get('isRedFlag')]
    if correct_objs:
        ans = ", ".join(correct_objs)
        collection.update_one({'_id': q['_id']}, {'$set': {'correctAnswer': ans}})
        print(f"Updated Q{q['id']} with {ans}")

print("Fix applied to MongoDB.")
