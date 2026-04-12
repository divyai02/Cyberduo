import json
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["cyberduo"]
questions_collection = db["questions"]

# Path to the JSON file
JSON_FILE = "../frontend/src/data/GameQuestions.json"

def migrate():
    if not os.path.exists(JSON_FILE):
        print(f"Error: {JSON_FILE} not found!")
        return

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Flatten the nested structure (gameKey -> level -> questions) into a list of documents
    documents = []
    
    for game_key, levels in data.items():
        for level, questions in levels.items():
            for q in questions:
                # Add metadata to each question document
                doc = q.copy()
                doc["game_key"] = game_key
                doc["level_name"] = level
                # Remove ID if it's just a number to let MongoDB handle it or keep it as local_id
                doc["local_id"] = doc.pop("id", None)
                documents.append(doc)

    if not documents:
        print("No questions found to migrate.")
        return

    # Clear existing questions to avoid duplicates on re-run
    questions_collection.delete_many({})
    
    # Insert all
    result = questions_collection.insert_many(documents)
    print(f"Successfully migrated {len(result.inserted_ids)} questions to MongoDB 'questions' collection.")

if __name__ == "__main__":
    migrate()
