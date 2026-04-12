import os
import json
import pymongo
from dotenv import load_dotenv
from bson import ObjectId

# Handle MongoDB ObjectId serialization
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)
db = client["cyberduo"]
collection = db["questions"]

def export_all_questions():
    print("Extracting all 375 questions from database...")
    
    # Sort by game, level, and local_id for readability
    all_questions = list(collection.find().sort([
        ("game_key", 1), 
        ("level_name", 1), 
        ("local_id", 1)
    ]))
    
    output_file = "all_cyberduo_questions.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=4, cls=JSONEncoder)
        
    print(f"SUCCESS: Exported {len(all_questions)} questions to {output_file}")
    print(f"Path: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    export_all_questions()
