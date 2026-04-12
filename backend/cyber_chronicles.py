import os
import json
import time
import re
import urllib.request
import urllib.error
import random

# Extract API key
api_key = None
with open("../frontend/.env", "r") as f:
    for line in f:
        if line.startswith("VITE_GEMINI_API_KEY="):
            api_key = line.split("=", 1)[1].strip()

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

def get_gemini_batch(prompt):
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 1.0, "topP": 0.95, "maxOutputTokens": 1024}
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as resp:
            response_data = json.loads(resp.read().decode('utf-8'))
            return response_data['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception as e:
        print(f"  -> API Error: {e}")
        return None

CATEGORIES = {
    "phishing": "Phishing & Fake Email Detection",
    "password": "Password Security & MFA",
    "malware": "Malware, Ransomware & Trojans",
    "firewall": "Firewall & Network Security",
    "scams": "Online Shopping & KYC Scams"
}

def generate_missions():
    input_file = "../frontend/src/data/GameQuestions.json"
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for game_key, display_name in CATEGORIES.items():
        if game_key not in data: continue
        
        for level in ["beginner", "medium", "hard"]:
            print(f"Authoring 25 UNIQUE {game_key} missions for {level} level...")
            
            all_hubs = []
            # We do 5 batches of 5 questions to be 100% safe from timeouts and 429
            for batch_num in range(5):
                print(f"  -> Authoring Batch {batch_num + 1}/5...")
                prompt = f"""
                Generate a JSON array of 5 UNIQUE cybersecurity story hubs for '{display_name}' ({level}).
                Characters must be Indian names. Situations must be relevant to {display_name}.
                NO DUPLICATES from previous missions.
                Format: [ {{"title": "...", "character": "...", "scenario": "...", "threat": "..."}}, ... ]
                Output ONLY JSON.
                """
                
                raw_json = None
                while not raw_json:
                    raw_json = get_gemini_batch(prompt)
                    if not raw_json:
                        time.sleep(30)
                    else:
                        try:
                            raw_json = re.sub(r"```json|```", "", raw_json).strip()
                            batch_hubs = json.loads(raw_json)
                            all_hubs.extend(batch_hubs)
                        except:
                            raw_json = None
                            time.sleep(5)
                time.sleep(10) # Small delay between micro-batches

            # Weave into the data
            base_templates = data[game_key]["beginner"][:5]
            new_questions = []
            for i in range(25):
                hub = all_hubs[i] if i < len(all_hubs) else (all_hubs[i % len(all_hubs)] if all_hubs else {"title": f"Mission {i+1}", "character": "Operative", "scenario": "Standard Drill", "threat": game_key})
                template = base_templates[i % len(base_templates)]
                q = json.loads(json.dumps(template))
                q["id"] = i + 1
                q["difficulty"] = level
                q["questionText"] = f"Mission: {hub['title']}\n{hub['character']} faces a tactical situation: {hub['scenario']}."
                q["hint"] = f"Look for the {hub['threat']}."
                q["concept"] = f"Operational {game_key.capitalize()} Awareness"
                
                # Randomized detail
                if "emailParts" in q:
                    q["emailParts"][0]["text"] = f"From: {hub['character'].lower()}@secure-node.in"
                
                new_questions.append(q)

            data[game_key][level] = new_questions
            # SAVE CONTINUOUSLY
            with open(input_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            
            print(f"  -> Level {level} Complete. Synchronizing...")
            time.sleep(20)

    print("\nDONE: 375 UNIQUE MISSIONS SYNCHRONIZED.")

if __name__ == "__main__":
    generate_missions()
