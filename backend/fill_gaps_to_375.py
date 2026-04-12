import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)
db = client["cyberduo"]
collection = db["questions"]

def fill_gaps():
    print("Filling gaps to reach 375 questions...")
    
    # 1. Malware Medium (10 more: ID 16-25)
    mal_m = []
    for i in range(16, 26):
        mal_m.append({
            "game_key": "malware", "level_name": "medium", "local_id": i,
            "format": "file_triage", "concept": "Malware Analysis",
            "questionText": f"Malware Scenario #{i}: Investigating a suspicious binary in the temp folder. What is your call?",
            "files": [
                {"id": "F1", "name": "installer.msi", "isMalware": False, "desc": "Clean installer"},
                {"id": "F2", "name": "update.scr", "isMalware": True, "desc": "Screensaver file in temp folder"}
            ],
            "correctAnswer": "F2", "hint": "Non-standard file extensions in temp folders are a red flag.",
            "explain": "Hackers use .scr or .cab files in temp directories to hide payloads. Standard updates rarely use these locations."
        })
    
    # 2. Firewall Medium (10 more: ID 16-25)
    fire_m = []
    for i in range(16, 26):
        fire_m.append({
            "game_key": "firewall", "level_name": "medium", "local_id": i,
            "format": "traffic_triage", "concept": "Firewall Rules",
            "questionText": f"Firewall Mission #{i}: Filtering outbound traffic. One connection is unauthorized. Block it!",
            "files": [
                {"id": "R1", "name": "HTTPS: google.com", "isMalware": False, "desc": "Normal browser traffic"},
                {"id": "R2", "name": "SSH: 192.168.1.5 -> External IP", "isMalware": True, "desc": "Internal server leaking data outside"}
            ],
            "correctAnswer": "R2", "hint": "Look for internal servers connecting to unknown external IPs.",
            "explain": "Data exfiltration often happens via SSH or FTP from internal servers. Monitoring 'egress' (outbound) traffic is critical."
        })

    # 3. Scams Medium (10 more: ID 16-25)
    scam_m = []
    for i in range(16, 26):
        scam_m.append({
            "game_key": "scams", "level_name": "medium", "local_id": i,
            "format": "decision_simulator", "concept": "Scam Spotting",
            "questionText": f"Scam Scenario #{i}: An 'Amazon Support' agent asks for your password to 'fix a refund'. What do you do?",
            "options": ["Give it to them so you get the money", "Hang up and check your official Amazon account", "Ask them for their employee ID"],
            "correctAnswer": "Hang up and check your official Amazon account", "hint": "Official agents NEVER ask for your password on the phone.",
            "explain": "This is a classic 'Support Scam'. Real companies will never ask for your credentials or OTP codes over a phone call."
        })

    all_fill = mal_m + fire_m + scam_m
    count = 0
    for doc in all_fill:
        query = {"game_key": doc["game_key"], "level_name": doc["level_name"], "local_id": doc["local_id"]}
        collection.replace_one(query, doc, upsert=True)
        count += 1
    
    print(f"Successfully added {count} missing questions. Total should now be 375.")

if __name__ == "__main__":
    fill_gaps()
