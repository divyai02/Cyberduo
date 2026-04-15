import os
import urllib.request
import urllib.parse
import json

# Manually load .env since python-dotenv might not be installed
news_key = None
try:
    with open(".env", "r") as f:
        for line in f:
            if line.startswith("NEWS_API_KEY="):
                news_key = line.split("=", 1)[1].strip()
except Exception as e:
    print(f"Error reading .env: {e}")

if not news_key:
    print("NEWS_API_KEY not found in .env!")
    exit(1)

print(f"Using News API Key: {news_key[:5]}...{news_key[-5:]}")

query = urllib.parse.quote('"cyber crime" OR cybercrime OR "online fraud" OR "digital arrest" OR hacker')
url = f"https://newsdata.io/api/1/news?apikey={news_key}&q={query}&country=in&language=en"

print(f"Requesting URL: {url}")

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')
        data = json.loads(content)
        print("Response Status:", data.get("status"))
        if data.get("status") == "success":
            results = data.get('results', [])
            print(f"Found {len(results)} results.")
            for i, result in enumerate(results[:3]):
                print(f"{i+1}. {result.get('title')}")
        else:
            print("Error Data:", data)
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
    try:
        error_body = e.read().decode()
        print(f"Error Body: {error_body}")
    except:
        pass
except Exception as e:
    print(f"News API Error: {e}")
