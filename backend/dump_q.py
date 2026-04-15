import os
import json
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["cyberduo"]

questions = list(db["questions"].find({"game_key": "phishing", "level_name": "beginner"}).sort("local_id", 1))
for q in questions:
    print(f"Q{q.get('local_id', q.get('id', '?'))}: {q.get('questionText')}")
    if q.get('format') == 'click_flags':
        print("  Opts:", [x['text'] for x in q.get('emailParts', [])])
    elif 'options' in q:
        print("  Opts:", q.get('options'))
    elif 'emails' in q:
        print("  Opts:", [x['subject'] for x in q.get('emails')])
    elif 'files' in q:
        print("  Opts:", [x['name'] for x in q.get('files')])
    elif 'objects' in q:
        print("  Opts:", [x['label'] for x in q.get('objects')])
    else:
        print("  Format:", q.get('format'))
