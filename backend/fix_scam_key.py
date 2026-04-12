import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)
db = client["cyberduo"]

def fix_scam_key():
    # Update scam_spotter -> scams
    res = db.questions.update_many(
        {"game_key": "scam_spotter"},
        {"$set": {"game_key": "scams"}}
    )
    print(f"Updated {res.modified_count} questions from 'scam_spotter' to 'scams'")

    # Also check if any 'malware' or 'firewall' need level_name sync
    # (Just in case)
    
    # Final count check
    count = db.questions.count_documents({"game_key": "scams", "level_name": "medium"})
    print(f"Scam Spotter (Medium) now has {count} questions in the DB.")

if __name__ == "__main__":
    fix_scam_key()
