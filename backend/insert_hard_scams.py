from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv('MONGO_URI'))
col = client['cyberduo']['questions']

# Clear existing hard scams
col.delete_many({'game_key': 'scams', 'level_name': 'hard'})

scams_hard = [
    {
        "local_id": 1, "format": "digital_whodunnit", "difficulty": "hard",
        "gameName": "scams", "game_key": "scams", "level_name": "hard",
        "concept": "NFT Wash Trading Detection",
        "hint": "Wash trading occurs when the same 'Owner' sells to themselves across different wallets to fake high value. Look for the wallet address that appears twice in the chain.",
        "explain": "NFT Scams often involve 'Wash Trading' where scammers buy their own NFT using different wallets to artificially inflate the price and create fake 'Hype'. Hard level requires tracing wallet addresses in a transaction chain.",
        "questionText": "Digital Whodunnit: Analyze the NFT transaction chain. One wallet address is 'Looping' to fake volume. Select the imposter wallet address that bought and sold the same item.",
        "correctAnswer": "0xAlpha...99",
        "emails": [
            {"id": "w1", "from": "0xAlpha...99", "spf": "BUYER", "dkim": "OFFER: 5 ETH"},
            {"id": "w2", "from": "0xBeta...12", "spf": "BUYER", "dkim": "OFFER: 12 ETH"},
            {"id": "w3", "from": "0xAlpha...99", "spf": "SELLER", "dkim": "SOLD: 15 ETH"}
        ]
    },
    {
        "local_id": 2, "format": "adversary_roleplay", "difficulty": "hard",
        "gameName": "scams", "game_key": "scams", "level_name": "hard",
        "concept": "Pig Butchering / Crypto Scams",
        "hint": "Scammers build rapport (trust) before asking for investment. Any 'Too Good To Be True' returns are a red flag.",
        "explain": "'Pig Butchering' is a long-term scam where victims are 'fattened up' with fake friendship before being 'slaughtered' (scammed for life savings). Hard level requires identifying the subtle psychological manipulation tactics used by professional scammers.",
        "budget": 5000,
        "targetValue": 90,
        "assets": [
            {"id": "s1", "name": "Withdraw All Funds Immediately", "cost": 0, "value": 100},
            {"id": "s2", "name": "Trust the 'Expert's' Advice", "cost": 2000, "value": -50},
            {"id": "s3", "name": "Verify Platform on Global Blacklist", "cost": 500, "value": 40}
        ],
        "questionText": "Scam Simulator: You've been chatting with a 'Crypto Guru' for weeks. They want you to invest $5000 in a 'Secret AI Token'. Choose your strategy to protect your assets."
    },
    {
        "local_id": 3, "format": "traffic_triage", "difficulty": "hard",
        "gameName": "scams", "game_key": "scams", "level_name": "hard",
        "concept": "Ponzi / Pyramid Scheme Analysis",
        "hint": "Analyze the 'Revenue Model'. If money only comes from 'New Members' and not a 'Product', it's a Ponzi scheme.",
        "explain": "Hard-level scams are disguised as 'Modern Business Opportunities'. Identifying the lack of a real product or service is key to spotting a multi-level marketing (MLM) pyramid or Ponzi scheme.",
        "files": [
            {"id": "m1", "name": "Level 1: Founders", "desc": "Revenue: Membership Fees", "isMalware": True},
            {"id": "m2", "name": "Level 2: Recruiters", "desc": "Revenue: Membership Fees", "isMalware": True},
            {"id": "m3", "name": "Retail Store", "desc": "Revenue: Real Product Sales", "isMalware": False}
        ],
        "questionText": "Business Triage: You are auditing 3 companies. BLOCK the 'Pyramid Schemes' (where revenue is only from fees) and ALLOW the legitimate business."
    },
    {
        "local_id": 4, "format": "click_flags", "difficulty": "hard",
        "gameName": "scams", "game_key": "scams", "level_name": "hard",
        "concept": "AI Deepfake Investment Scam",
        "hint": "Look for AI-generated artifacts: glitchy eyes, monotone voice transcripts, and 'Guaranteed' profit claims from 'Elon Musk' or 'Celebrities'.",
        "explain": "Deepfake video scams use AI to impersonate celebrities promising to double your crypto. Hard level awareness means spotting the 'Glitchy' quality and the mathematical impossibility of 'Doubling your money instantly'.",
        "emailParts": [
            {"id": "p1", "text": "VIDEO: Elon Musk announces new Tesla Coin!", "isFlag": False},
            {"id": "p2", "text": "PROMISE: Send 1 ETH, get 2 ETH back instantly!", "isFlag": True},
            {"id": "p3", "text": "Notice: AI-generated lip-sync artifacts detected.", "isFlag": True},
            {"id": "p4", "text": "Payment to: Unknown Russian Crypto Wallet", "isFlag": True}
        ],
        "correctAnswer": "Click: Impossible Returns, AI Glitches, Suspicious Wallet",
        "questionText": "Scam Spotter: You see a viral video on YouTube. Click the 3 red flags that prove this is a sophisticated AI Deepfake scam."
    },
    {
        "local_id": 5, "format": "scavenger_hunt", "difficulty": "hard",
        "gameName": "scams", "game_key": "scams", "level_name": "hard",
        "concept": "Romance Scam / Catfishing",
        "hint": "Check the profile photos. If they look like 'Stock Photos' or 'Models', it's likely a fake profile.",
        "explain": "Romance scammers (Catfish) use attractive photos and emotional stories to steal money. Hard level requires finding the 'Inconsistencies' in their digital footprint.",
        "objects": [
            {"id": "o1", "icon": "📸", "label": "Profile Pic: Professional Model (Stock Photo)", "isRedFlag": True},
            {"id": "o2", "icon": "💬", "label": "Message: 'I'm stuck in a foreign hospital, send $500'", "isRedFlag": True},
            {"id": "o3", "icon": "🏢", "label": "Bio: Claims to be a CEO but has no LinkedIn", "isRedFlag": True},
            {"id": "o4", "icon": "📍", "label": "Location: London (verified)", "isRedFlag": False}
        ],
        "questionText": "Catfish Hunter: You're helping a friend audit a new online match. Click on all the 'Fake Profile' red flags you can find."
    }
]

# Fill remaining 20 Scams Hard
for i in range(6, 26):
    scams_hard.append({
        "local_id": i, "format": "traffic_triage", "difficulty": "hard",
        "gameName": "scams", "game_key": "scams", "level_name": "hard",
        "concept": "Gift Card / Refund Scams",
        "hint": "Any 'Government Agency' or 'Big Tech' company asking for payment in Gift Cards (Steam, Apple) is a 100% scam.",
        "explain": "Hard level scams often impersonate the IRS or Microsoft. They demand payment via untraceable Gift Cards. Real agencies never accept these as legal tender.",
        "files": [
            {"id": f"s{i}1", "name": "Payment Method", "desc": "Steam Gift Card Codes", "isMalware": True},
            {"id": f"s{i}2", "name": "Refund Link", "desc": "Download 'Refund-Tool.exe'", "isMalware": True},
            {"id": f"s{i}3", "name": "Support Ticket", "desc": "Official Case #1029", "isMalware": False}
        ],
        "questionText": f"Mission {i}: Tech Support Triage. A 'Microsoft Agent' is on the phone. Sort these requests: BLOCK the scam actions and ALLOW legitimate support."
    })

col.insert_many(scams_hard)

print(f"Inserted 25 Scams Hard missions.")
client.close()
