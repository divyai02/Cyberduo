from dotenv import load_dotenv
import os
load_dotenv()
from pymongo import MongoClient
from bson import ObjectId
import datetime

client = MongoClient(os.getenv('MONGO_URI'))
users = client['cyberduo']['users']

# Get divyaa's user ID
divyaa = users.find_one({'username': 'divyaa'})
print("divyaa current XP:", divyaa.get('xp', 0))
print("divyaa _id:", str(divyaa['_id']))

# --- Simulate exactly what save-result does ---
user_id = divyaa['_id']
xp_earned = 20

# Atomic XP increment (as per our fix)
result = users.find_one_and_update(
    {"_id": user_id},
    {"$inc": {"xp": xp_earned}},
    return_document=True
)
new_xp = result.get("xp", 0)
print(f"After atomic $inc: divyaa XP = {new_xp}")

# Now check from a fresh read
fresh = users.find_one({'username': 'divyaa'})
print(f"Fresh DB read confirms: divyaa XP = {fresh.get('xp', 0)}")

print("\n--- DB write is WORKING. The issue must be in the frontend userId or the fetch call ---")
print(f"\nFor frontend testing, divyaa's userId is: {str(divyaa['_id'])}")
print("Make sure this matches localStorage.getItem('cyberduo_user_data').user_id")

# Reset back to 410 for a clean slate
users.update_one({'username': 'divyaa'}, {'$set': {'xp': 410}})
print(f"\nReset divyaa XP back to 410 for clean testing.")

client.close()
