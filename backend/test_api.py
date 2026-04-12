import urllib.request
import json

# Extract API key
api_key = None
try:
    with open("../frontend/.env", "r") as f:
        for line in f:
            if line.startswith("VITE_GEMINI_API_KEY="):
                api_key = line.split("=", 1)[1].strip()
except Exception as e:
    print(f"Error reading .env: {e}")

if not api_key:
    print("API Key not found!")
else:
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    print(f"Checking: {url}")
    try:
        with urllib.request.urlopen(url) as resp:
            content = resp.read().decode('utf-8')
            data = json.loads(content)
            with open("api_response.json", "w") as out:
                json.dump(data, out, indent=2)
            print("Successfully saved response to api_response.json")
    except Exception as e:
        print(f"Error: {e}")
