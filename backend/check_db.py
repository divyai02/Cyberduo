from dotenv import load_dotenv
import os
load_dotenv()
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient(os.getenv('MONGO_URI'))
users = client['cyberduo']['users']

# Show all users with their current XP in DB
print("=== CURRENT XP IN DATABASE ===")
all_users = list(users.find({}, {"username": 1, "xp": 1, "games_completed": 1, "xp_awarded_questions": 1}))
for u in all_users:
    name = u.get("username", "?")
    xp = u.get("xp", 0)
    completed = u.get("games_completed", [])
    print(f"  {name}: {xp} XP | completed games: {completed}")

print(f"\nTotal users: {len(all_users)}")
client.close()
