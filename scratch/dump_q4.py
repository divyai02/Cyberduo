from pymongo import MongoClient
import os
from dotenv import load_dotenv
import json

load_dotenv('backend/.env')
client = MongoClient(os.getenv('MONGO_URI'))
db = client['cyberduo']
col = db['questions']

q = col.find_one({'game_key': 'phishing', 'level_name': 'hard', 'local_id': 4})
print(json.dumps(q, indent=2, default=str))

client.close()
