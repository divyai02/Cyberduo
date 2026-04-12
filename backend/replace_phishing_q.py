from dotenv import load_dotenv
import os
load_dotenv()
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGO_URI'))
col = client['cyberduo']['questions']

# Remove the 3 "identify phishing email" questions: Q1 (adaptive_inbox), Q6 (inbox_triage), Q13 (adaptive_inbox)
col.delete_many({'game_key': 'phishing', 'level_name': 'beginner', 'local_id': {'$in': [1, 6, 13]}})

new_questions = [

    # Q1 — digital_whodunnit: "Email Header Murder Mystery"
    # Completely new format - user reads a spoofed email header table and spots the forgery
    {
        "local_id": 1,
        "format": "digital_whodunnit",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Email Header Spoofing",
        "hint": "The 'From' display name and the actual SMTP 'Return-Path' address do NOT have to match. Check if both are from the same real domain!",
        "explain": "Every email has a visible 'From' label AND a hidden technical 'Return-Path' that shows where replies actually go. Hackers can make the display name say 'PayPal Support' while the real sending address is a completely different domain. Looking at the full header reveals the truth!",
        "reveal": "The forgery is in the Return-Path! It shows 'paypal-security@mail-alert.ru' — a Russian domain, nothing to do with PayPal. Real PayPal emails always originate from @paypal.com domains. The display name 'PayPal Security' was just a disguise painted over a fake address.",
        "correctAnswer": "Return-Path: paypal-security@mail-alert.ru (Russian domain — NOT PayPal!)",
        "questionText": "Email Header Murder Mystery! A suspicious PayPal email has arrived. Study the email header clues below and identify the ONE field that proves it is fake:",
        "headers": [
            {"field": "From (Display)", "value": "PayPal Security <paypal-security@mail-alert.ru>", "isSuspicious": True},
            {"field": "To", "value": "you@yourmail.com", "isSuspicious": False},
            {"field": "Subject", "value": "Your PayPal account is limited!", "isSuspicious": False},
            {"field": "Date", "value": "Mon, 10 Apr 2026 03:22:11 +0000", "isSuspicious": False},
            {"field": "Return-Path", "value": "paypal-security@mail-alert.ru", "isSuspicious": True}
        ],
        "options": [
            "The 'To' field — it shows your real email address",
            "The 'Return-Path' field — it shows the email actually came from a Russian domain, not PayPal",
            "The 'Date' field — emails at 3am are always suspicious",
            "The 'Subject' field — it mentions account limitations"
        ],
        "correctAnswer": "The 'Return-Path' field — it shows the email actually came from a Russian domain, not PayPal"
    },

    # Q6 — case_study: "The Phishing Crime Scene"
    # New format - a rich scenario card with a browser screenshot, MCQ about what happened
    {
        "local_id": 6,
        "format": "case_study",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Recognising a Phishing Website",
        "hint": "Look at the URL bar first. Does it say 'https' and the exact correct domain? A padlock alone does NOT guarantee a site is real!",
        "explain": "Phishing websites look identical to real ones — same logo, same colours, same layout. The ONLY reliable way to detect them is the URL bar. Attackers register domains that look similar (like 'amaz0n.com') and even get HTTPS certificates for them. The padlock icon means the connection is encrypted — not that the site is legitimate!",
        "reveal": "The crime scene: the URL 'amaz0n-secure-login.com' used a zero (0) instead of an 'o' — a classic homograph/typosquatting attack. The green padlock just means the fake site has a certificate, NOT that it is safe. The victim typed their real Amazon password into a fake page!",
        "correctAnswer": "The URL 'amaz0n-secure-login.com' uses a zero instead of the letter 'o' — a fake domain!",
        "questionText": "The Phishing Crime Scene! You receive an email with a link to log in to Amazon. The browser shows this address. What is the biggest red flag?",
        "scenario": "Browser Address Bar shows: https://amaz0n-secure-login.com/signin\nPage looks: Identical copy of Amazon login page with logo and green padlock icon\nEmail Subject: 'Your Amazon order has a delivery issue! Log in to resolve it'\nResult: Victim enters their real Amazon password",
        "redFlags": [
            "The URL uses 'amaz0n' with a zero (0) instead of the letter 'o' — it is a fake domain",
            "The green padlock icon means the fake site is encrypted, NOT that it is Amazon",
            "The email creates urgency with a 'delivery issue' to make you act without thinking",
            "The domain is 'amaz0n-secure-login.com' — Amazon would never use a hyphenated subdomain like this"
        ],
        "options": [
            "The URL uses 'amaz0n' with a zero instead of a letter 'o' — this is a fake copycat domain",
            "The email was found in your inbox — all inbox emails are legitimate",
            "The green padlock next to the URL guarantees the website is the real Amazon",
            "Delivery issue emails are always real because Amazon sends them regularly"
        ],
        "correctAnswer": "The URL uses 'amaz0n' with a zero instead of a letter 'o' — this is a fake copycat domain",
        "correctFlags": [
            "The URL uses 'amaz0n' with a zero (0) instead of the letter 'o' — it is a fake domain",
            "The green padlock icon means the fake site is encrypted, NOT that it is Amazon",
            "The email creates urgency with a 'delivery issue' to make you act without thinking",
            "The domain is 'amaz0n-secure-login.com' — Amazon would never use a hyphenated subdomain like this"
        ]
    },

    # Q13 — traffic_triage: "Suspicious Network Traffic Inspector"
    # Brand new format - user reads 3 network-like "connection logs" and flags the suspicious ones
    {
        "local_id": 13,
        "format": "traffic_triage",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Recognising Phishing Traffic Patterns",
        "hint": "Legitimate websites use their real company domain. Suspicious connections go to random domains you've never heard of, especially after clicking an email link.",
        "explain": "When you click a phishing link, your computer secretly connects to the attacker's server to send your data. A network traffic log shows these hidden connections. Security teams use these logs daily to catch phishing attacks in progress before too much damage is done!",
        "reveal": "The two suspicious connections were: 'steal-creds.xyz' (an obvious data-harvesting domain that your browser connected to after clicking a link!) and 'tracking.phish-ops.net' (a known phishing infrastructure domain). The connection to 'microsoft.com' was totally normal Windows update traffic.",
        "correctAnswer": "Flag: steal-creds.xyz and tracking.phish-ops.net — both are phishing infrastructure domains",
        "questionText": "Network Traffic Inspector! After clicking a suspicious link in an email, these 3 outgoing connections appeared in the log. Which ones are PHISHING traffic? Mark all suspicious ones as PHISH:",
        "traffic": [
            {"id": "t1", "source": "Your PC", "destination": "steal-creds.xyz:443", "data": "POST /collect?user=you&pass=****", "isPhish": True},
            {"id": "t2", "source": "Your PC", "destination": "microsoft.com:443", "data": "GET /updates/win11-patch.msi", "isPhish": False},
            {"id": "t3", "source": "Your PC", "destination": "tracking.phish-ops.net:80", "data": "GET /beacon?id=victim_001", "isPhish": True}
        ]
    }
]

result = col.insert_many(new_questions)
total = col.count_documents({'game_key': 'phishing', 'level_name': 'beginner'})
print("Inserted " + str(len(result.inserted_ids)) + " new phishing questions")
print("Total phishing beginner questions: " + str(total))

# Show all formats to confirm no consecutive duplicates
docs = list(col.find({'game_key': 'phishing', 'level_name': 'beginner'}, {'local_id': 1, 'format': 1, '_id': 0}).sort('local_id', 1))
print("\nFinal question list:")
for d in docs:
    print("  Q" + str(d.get('local_id','?')).rjust(2) + ": " + str(d.get('format','?')))

client.close()
