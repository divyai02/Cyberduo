import os
import json
import time
import re
import urllib.request
import urllib.error

# Load key from frontend .env manually to avoid dotenv dependency issues if missing
api_key = None
with open("../frontend/.env", "r") as f:
    for line in f:
        if line.startswith("VITE_GEMINI_API_KEY="):
            api_key = line.split("=", 1)[1].strip()

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

input_file = "../frontend/src/data/GameQuestions.json"
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

for game_name in data.keys():
    for level in ["beginner", "medium", "hard"]:
        # Skip if already expanded to 25 unique items (avoid re-spending API tokens)
        if len(data[game_name].get(level, [])) >= 25:
            print(f"Skipping '{game_name}' ({level}) - already has {len(data[game_name][level])} questions.")
            continue

        # Extract the original 5 handcrafted templates to guarantee structural UI safety
        # If we already have some questions, we still start from the beginner templates for safety
        templates = data[game_name]["beginner"][:5]
        
        # We need 20 more questions.
        new_batch = []
        for start_id in [6, 16]:
            prompt = f"""
            You are an expert cybersecurity scenario writer. Your task is to generate 10 NEW, highly unique, storytelling-based questions for a React.js game called '{game_name}' at the '{level}' difficulty level.
            
            Here are 5 JSON templates showing the EXACT UI formats supported.
            {json.dumps(templates, indent=2)}
            
            Using EXACTLY the mechanics/formats found above (never invent new formats), generate a JSON array of 10 COMPLETELY NEW and UNIQUE questions.
            - Ensure names, companies, concepts, industries, and scenarios are extremely varied (e.g. healthcare, startup, family, finance).
            - For 'medium' and 'hard' difficulties, the tricks must be harder to spot (e.g. very subtle email domain typos like .co, extremely convincing spear-phishing lures, tricky file extensions).
            - Start 'id' exactly from {start_id} to {start_id+9}.
            - Set 'difficulty' to '{level}'.
            - ONLY Output a pure JSON array starting with [ and ending with ]. Do NOT wrap in markdown or add explanations.
            """
            
            print(f"Requesting '{game_name}' ({level}) batch IDs {start_id}-{start_id+9}...")
            
            success = False
            retries = 10  # Very high retries for rate limits
            while not success and retries > 0:
                try:
                    payload = json.dumps({
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {
                            "temperature": 0.9,
                            "topP": 0.95,
                            "maxOutputTokens": 4096
                        }
                    }).encode('utf-8')
                    
                    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
                    with urllib.request.urlopen(req) as resp:
                        response_data = json.loads(resp.read().decode('utf-8'))
                        raw = response_data['candidates'][0]['content']['parts'][0]['text'].strip()
                    
                    # Clean markdown
                    if raw.startswith("```json"): raw = raw[7:]
                    elif raw.startswith("```"): raw = raw[3:]
                    if raw.endswith("```"): raw = raw[:-3]
                    raw = raw.strip()
                    
                    # Final safety regex to grab just the array
                    match = re.search(r"\[.*\]", raw, re.DOTALL)
                    if match:
                        raw = match.group(0)
                        
                    parsed = json.loads(raw)
                    if isinstance(parsed, list) and len(parsed) > 0:
                        new_batch.extend(parsed)
                        success = True
                        print(f"  -> Success. Batch of {len(parsed)} received.")
                    else:
                        print(f"  -> Warning: Received invalid response. Retrying...")
                        retries -= 1
                except urllib.error.HTTPError as e:
                    if e.code == 429:
                        print(f"  -> Rate Limited (429). Sleeping 60s...")
                        time.sleep(60)
                    else:
                        print(f"  -> HTTP Error {e.code}: {e.reason}... Retrying...")
                        time.sleep(10)
                    retries -= 1
                except Exception as e:
                    print(f"  -> Error: {str(e)[:100]}... Retrying...")
                    retries -= 1
                    time.sleep(10)
            
            if success:
                # Save progress after every batch to be resumable
                final_list = templates + new_batch
                data[game_name][level] = final_list
                with open(input_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                
                print(f"  -> Cooling down 20s...")
                time.sleep(20)
            else:
                print(f"!! FAILED batch for {game_name} ({level}). Moving to next...")

print("MASSIVE AI GENERATION PROCESS COMPLETE!")
