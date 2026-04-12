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

# Load the local json with the rich explanations
filepath = r'frontend\src\data\GameQuestions.json'
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Clear existing phishing beginner questions in mongo
collection.delete_many({'game_key': 'phishing', 'level_name': 'beginner'})

# Insert the refreshed beginner questions
docs = data['phishing']['beginner']
for q in docs:
    q['game_key'] = 'phishing'
    q['level_name'] = 'beginner'
    collection.insert_one(q)

print(f"MongoDB synchronized successfully with {len(docs)} distinct questions.")
