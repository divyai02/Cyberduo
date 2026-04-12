import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)
db = client["cyberduo"]

def audit():
    print("--- DB AUDIT START ---")
    games = db.questions.distinct("game_key")
    for g in games:
        levels = db.questions.distinct("level_name", {"game_key": g})
        print(f"Game Key: {g}")
        for l in levels:
            count = db.questions.count_documents({"game_key": g, "level_name": l})
            print(f"  - Level: {l} ({count} questions)")
    
    print("\n--- FRONTEND KEYS CHECK ---")
    frontend_keys = ["phishing", "password", "malware", "firewall", "scams"]
    for fk in frontend_keys:
        exists = fk in games
        print(f"Frontend Key '{fk}' exists in DB: {exists}")
    print("--- DB AUDIT END ---")

if __name__ == "__main__":
    audit()
