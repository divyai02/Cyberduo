import json
import random

input_file = "src/data/GameQuestions.json"

def get_whodunit(game, level, q_id):
    scenarios = {
        "phishing": {
            "title": "Detective Mission: The Email Imposter",
            "story": "A suspicious email was sent to the finance team late at night. Examine the message details and identify the security risks.",
            "parts": [
                {"id": "h1", "text": "From: Internal Office <support@hacker-portal.com>", "isFlag": True},
                {"id": "h2", "text": "To: Accounts <finance@company.com>", "isFlag": False},
                {"id": "h3", "text": "Subject: Outstanding Payment - Action Required", "isFlag": True},
                {"id": "h4", "text": "Sent: Saturday, 3:15 AM", "isFlag": True}
            ],
            "hint": "Official support rarely uses a '.com' domain if they have a company portal. Also, check the time.",
            "explain": "Professional hackers send emails during 'off-hours' (like 3 AM) when you are tired and less likely to double-check.",
            "reveal": "The red flags were the third-party domain, the urgent subject, and the 3 AM delivery time.",
            "correctAnswer": "Strange Sender Domain + Urgent Subject + 3 AM Timestamp"
        },
        "password": {
            "title": "Detective Mission: Brute Force Logs",
            "story": "The server logs show someone is trying to force their way into an account. Find the evidence of the attack.",
            "parts": [
                {"id": "l1", "text": "Login Fail: 100 attempts in 30 seconds", "isFlag": True},
                {"id": "l2", "text": "IP Origin: Multiple Unknown Locations", "isFlag": True},
                {"id": "l3", "text": "System Status: Firewall Active", "isFlag": False}
            ],
            "hint": "Look for a high number of failures in a very short amount of time.",
            "explain": "A human cannot try 100 passwords in 30 seconds. This is a computer-automated attack.",
            "reveal": "High-frequency login failures and multiple IP locations are sure signs of a brute force attack.",
            "correctAnswer": "100 failures in 30s + Multiple IP Locations"
        },
        "malware": {
            "title": "Detective Mission: The Ghost Program",
            "story": "A user's computer is acting strange after a 'Software Update'. Find the signs of an infection.",
            "parts": [
                {"id": "p1", "text": "System running at 99% CPU load", "isFlag": True},
                {"id": "p2", "text": "New unknown file: system_crypt.exe", "isFlag": True},
                {"id": "p3", "text": "Antivirus: Scan Complete (Clean)", "isFlag": False}
            ],
            "hint": "Look for new files you didn't install and high computer usage.",
            "explain": "Malware often uses high processing power to encrypt your files or mine cryptocurrency in the background.",
            "reveal": "The 99% CPU load and the unknown '.exe' file indicate a malware infection.",
            "correctAnswer": "99% CPU Load + unknown .exe file"
        },
        "scams": {
            "title": "Detective Mission: The UPI Trap",
            "story": "A student received a message about a government scholarship. Look for the common scam indicators.",
            "parts": [
                {"id": "c1", "text": "Sender: +91 00000 00000 (Unknown)", "isFlag": True},
                {"id": "c2", "text": "Message: 'Scan this code to RECEIVE money'", "isFlag": True},
                {"id": "c3", "text": "Link: govt-scholarship-v3.xyz", "isFlag": True}
            ],
            "hint": "Remember: You never need to enter a PIN or scan a QR code to RECEIVE money.",
            "explain": "Scammers trick people into scanning 'receive' codes that actually deduct money from their account.",
            "reveal": "QR codes are for sending money. Asking to scan one to 'receive' is a 100% confirmed scam.",
            "correctAnswer": "QR Code to Receive + Unknown Number + .xyz Link"
        },
        "firewall": {
            "title": "Detective Mission: The Port Probe",
            "story": "Your home security system detected someone trying to 'knock' on your network doors. Identify the risk.",
            "parts": [
                {"id": "f1", "text": "Source: Unregistered IP 185.x.x.x", "isFlag": True},
                {"id": "f2", "text": "Action: Probing 500 secret ports", "isFlag": True},
                {"id": "f3", "text": "Device: Smart Refrigerator (Normal)", "isFlag": False}
            ],
            "hint": "An unknown IP 'knocking' on many ports is looking for an open vulnerability.",
            "explain": "Hackers 'probe' ports to see which ones are open to attack. An unregistered foreign IP doing this is dangerous.",
            "reveal": "The unknown IP and the probing of 500 ports were the clear signs of an intruder.",
            "correctAnswer": "Unregistered IP + Probing 500 Ports"
        }
    }
    sc = scenarios.get(game, scenarios["phishing"])
    return {
        "id": q_id, "format": "click_flags", "difficulty": level, "gameName": game,
        "questionText": f"{sc['title']} - {sc['story']}",
        "emailParts": sc["parts"], "concept": "Identify Red Flags",
        "hint": sc["hint"], "explain": sc["explain"], "reveal": sc["reveal"],
        "correctAnswer": sc["correctAnswer"]
    }

def get_reverse_engineering(game, level, q_id):
    scenarios = {
        "phishing": {
            "target": "School Principal",
            "lures": [
                {"text": "Hey, watch this funny cat video!", "correct": False},
                {"text": "Official: Updated Education Safety Policy", "correct": True}
            ],
            "urgencies": [
                {"text": "Read this when you are free.", "correct": False},
                {"text": "Review and Sign by 4 PM today.", "correct": True}
            ],
            "explain": "Attacker Strategy: Professionals use role-based lures. A Principal is much more likely to click a 'Safety Policy' than a 'Cat Video'."
        },
        "password": {
            "target": "Online Gamer",
            "lures": [
                {"text": "Free Pizza delivery!", "correct": False},
                {"text": "Warning: Rare in-game items about to expire", "correct": True}
            ],
            "urgencies": [
                {"text": "Check it out tomorrow.", "correct": False},
                {"text": "Login in 10 minutes to claim.", "correct": True}
            ],
            "explain": "Attacker Strategy: Scammers create a 'Fear of Missing Out' (FOMO). Gamers don't want to lose rare items, making them act fast."
        },
        "malware": {
            "target": "New Employee",
            "lures": [
                {"text": "Company Picnic Photos", "correct": False},
                {"text": "Required: Payroll Enrollment Form (Direct Deposit)", "correct": True}
            ],
            "urgencies": [
                {"text": "Submit when convenient.", "correct": False},
                {"text": "Complete within 1 hour to get paid this week.", "correct": True}
            ],
            "explain": "Attacker Strategy: Everyone wants to get paid. A payroll link creates high trust and high urgency for a new hire."
        },
        "scams": {
            "target": "Frequent Shopper",
            "lures": [
                {"text": "We found your lost keys!", "correct": False},
                {"text": "Order Blocked: Payment Error on your Recent Buy", "correct": True}
            ],
            "urgencies": [
                {"text": "Resolve at your leisure.", "correct": False},
                {"text": "Fix Payment in 15 mins to avoid cancellation.", "correct": True}
            ],
            "explain": "Attacker Strategy: By targeting 'Recent Purchases', scammers increase the odds that the victim is actually waiting for a delivery."
        },
        "firewall": {
            "target": "Remote IT Worker",
            "lures": [
                {"text": "Check out these funny code bugs.", "correct": False},
                {"text": "Security Breach Alert: Reset VPN Certificate", "correct": True}
            ],
            "urgencies": [
                {"text": "Update by next month.", "correct": False},
                {"text": "Update NOW to prevent server loss.", "correct": True}
            ],
            "explain": "Attacker Strategy: IT workers take 'Security Breaches' seriously. Using their own professional language makes the trap believable."
        }
    }
    sc = scenarios.get(game, scenarios["phishing"])
    correct_lure = [l['text'] for l in sc['lures'] if l['correct']][0]
    correct_urgency = [u['text'] for u in sc['urgencies'] if u['correct']][0]
    
    return {
        "id": q_id, "format": "build_phish", "difficulty": level, "gameName": game,
        "questionText": f"HACKER STRATEGY: You are the attacker. Choose the most effective trap for the {sc['target']}.",
        "lures": sc["lures"], "urgencies": sc["urgencies"],
        "concept": "Understanding Tactics",
        "hint": f"What is the top priority for a {sc['target']}? Hit them where it matters.",
        "explain": sc["explain"], "reveal": "Excellent analysis. You now understand how hackers plan their social engineering attacks.",
        "correctAnswer": f"'{correct_lure}' with '{correct_urgency}'"
    }

def get_inject(game, level, q_id):
    scenarios = {
        "phishing": {
            "q": "A 'Hacked' message just appeared on your home computer! It asks for money to unlock your photos.",
            "ops": ["Don't touch it", "Turn off the Wi-Fi immediately", "Pay the money to be safe"],
            "ans": "Turn off the Wi-Fi immediately",
            "exp": "Cutting the internet is the best first step. It stops the attacker from seeing your files further."
        },
        "password": {
            "q": "Your phone is suddenly receiving 50 messages asking you to 'Approve Login' from an unknown device.",
            "ops": ["Approve one to see who it is", "Ignore it", "Say NO and change your password NOW"],
            "ans": "Say NO and change your password NOW",
            "exp": "This means someone already has your password! Say NO to stop them, then change your password so they can't try again."
        },
        "malware": {
            "q": "Your computer mouse is moving by itself and opening folders while you watch!",
            "ops": ["Pull out the internet cable", "Watch what it does", "Restart the computer"],
            "ans": "Pull out the internet cable",
            "exp": "If the mouse is moving, a hacker is 'remote controlling' you. Pulling the cable kicks them out of your computer instantly."
        },
        "scams": {
            "q": "A person on a video call says they are a Police Officer and you must pay a fine on UPI right now.",
            "ops": ["Pay the fine to avoid trouble", "Record the video", "Hang up and call the real 112/100 police"],
            "ans": "Hang up and call the real 112/100 police",
            "exp": "Real police never ask for money on UPI or video calls. Hang up and call the official emergency number to stay safe."
        },
        "firewall": {
            "q": "Your Wi-Fi is suddenly very slow because thousands of strangers are trying to connect at once from another country.",
            "ops": ["Block visitors from that country", "Restart your router", "Wait for it to stop"],
            "ans": "Block visitors from that country",
            "exp": "Blocking 'foreign' traffic stops the attack from reaching your house while keeping your own internet working."
        }
    }
    sc = scenarios.get(game, scenarios["phishing"])
    return {
        "id": q_id, "format": "decision_simulator", "difficulty": level, "gameName": game,
        "questionText": f"QUICK DECISION: {sc['q']}",
        "options": sc["ops"], "correctAnswer": sc["ans"],
        "concept": "Acting Fast",
        "hint": "Stopping the connection is usually the best first step.",
        "explain": sc["exp"], "reveal": "Safe! Your quick action saved your data.",
    }

def get_spot_difference(game, level, q_id):
    sc_text = {
        "phishing": "Look at these two links. Which one is a FAKE meant to trick you?\n\n1. amazon.in\n2. amaz0n.in (with a Zero)",
        "password": "Which username looks fake and suspicious in a system log?\n\n1. admin_rk\n2. h@cker_123",
        "malware": "Which file is actually a hidden program that could harm your PC?\n\n1. MyPhoto.jpg\n2. MyPhoto.jpg.exe",
        "scams": "Which bank support email is a fake?\n\n1. alerts@hdfcbank.com\n2. help@hdfc-money-secure.net",
        "firewall": "Which IP address looks impossible and fake?\n\n1. 192.168.1.1\n2. 999.999.9.9"
    }
    ans = { "phishing": "2. amaz0n.in (with a Zero)", "password": "2. h@cker_123", "malware": "2. MyPhoto.jpg.exe", "scams": "2. help@hdfc-money-secure.net", "firewall": "2. 999.999.9.9" }
    return {
        "id": q_id, "format": "decision_simulator", "difficulty": level, "gameName": game,
        "questionText": "SPOT THE MISTAKE: " + sc_text.get(game, ""),
        "options": ["1", "2"],
        "correctAnswer": ans.get(game, "2"),
        "concept": "Detail-Oriented",
        "hint": "Look for numbers (0) being used instead of letters (O).",
        "explain": "Scammers change one tiny letter in a name so you don't notice the difference.",
        "reveal": "Correct! You have a great eye for security traps."
    }

def get_crypto_logic(game, level, q_id):
    return {
        "id": q_id, "format": "sequence_builder", "difficulty": level, "gameName": game,
        "questionText": "SECURITY PROTOCOL: How do you safely open an encrypted (locked) file from a new sender?",
        "steps": [
            {"id": "1", "text": "Check who sent it.", "correctOrder": 0},
            {"id": "2", "text": "Verify identity via phone call.", "correctOrder": 1},
            {"id": "3", "text": "Enter the secret key.", "correctOrder": 2},
            {"id": "4", "text": "Read the file.", "correctOrder": 3}
        ],
        "concept": "Safety Steps",
        "hint": "Communication always happens before you open a locked file.",
        "explain": "Opening a locked file from a stranger is dangerous. Always verify through a second channel first.",
        "reveal": "Protocol complete. You followed the safest path to data access.",
        "correctAnswer": "Check -> Verify -> Key -> Read"
    }

def get_insider_threat(game, level, q_id):
    return {
        "id": q_id, "format": "select_all", "difficulty": level, "gameName": game,
        "questionText": "INTERNAL AUDIT: Which of these employee behaviors are suspicious and risky?",
        "options": [
            "A) Downloading massive amounts of data at midnight",
            "B) Asking IT to reset their password",
            "C) Accessing folders they don't need for their job",
            "D) Attending a company meeting"
        ],
        "correctFlags": ["A) Downloading massive amounts of data at midnight", "C) Accessing folders they don't need for their job"],
        "concept": "Behavioral Red Flags",
        "hint": "Look for activity at weird times or in places they shouldn't be.",
        "explain": "Hacking often leaves a trail of strange behavior. Real employees usually work during normal hours and only use their own folders.",
        "reveal": "Audit success! You identified the internal risks correctly.",
        "correctAnswer": "A) Data at Midnight + C) Unneeded Folder Access"
    }

def generate_standard_narrative(game, level, q_id):
    char = random.choice(["Maya", "Ishaan", "Arjun", "Aditya", "Riya", "Sahil", "Aditi", "Vivek"])
    brands = ["Flipkart", "Jio", "Zomato", "Microsoft", "Meta", "Google", "PhonePe"]
    brand = random.choice(brands)
    
    scenarios = [
        f"{char} got a text about a {brand} balance update. What is the safest move?",
        f"A popup says {char} won a free prize from {brand}. Is it real?",
        f"{char} found an official-looking {brand} USB in the parking lot. Should they plug it in?",
        f"Someone from '{brand} Support' called asking for an OTP over the phone. Give it?"
    ]
    
    return {
        "id": q_id, "format": "decision_simulator", "difficulty": level, "gameName": game,
        "questionText": f"SAFE DECISION: {random.choice(scenarios)}",
        "options": ["Don't click, report it", "Click and see what happens", "Ignore it"],
        "correctAnswer": "Don't click, report it",
        "concept": "Standard Safety",
        "hint": "If it asks for a code or money, it's likely a scam.",
        "explain": f"Always check the official {brand} website directly. Never trust links from sudden texts or popups.",
        "reveal": "Correct decision. You successfully identified a common social engineering tactic.",
        "correctAnswer": "Don't click, report it"
    }

def build_game_questions(game):
    final_questions = { "beginner": [], "medium": [], "hard": [] }
    for level in ["beginner", "medium", "hard"]:
        lvl_list = []
        lvl_list.append(get_whodunit(game, level, 1))
        lvl_list.append(get_reverse_engineering(game, level, 2))
        lvl_list.append(get_inject(game, level, 3))
        lvl_list.append(get_spot_difference(game, level, 4))
        lvl_list.append(get_crypto_logic(game, level, 5))
        lvl_list.append(get_insider_threat(game, level, 6))
        lvl_list.append(get_whodunit(game, level, 7))
        lvl_list.append(get_reverse_engineering(game, level, 8))
        lvl_list.append(get_inject(game, level, 9))
        lvl_list.append(get_spot_difference(game, level, 10))
        for i in range(11, 26):
            lvl_list.append(generate_standard_narrative(game, level, i))
        final_questions[level] = lvl_list
    return final_questions

def run_reconstruction():
    games = ["phishing", "password", "malware", "scams", "firewall"]
    final_database = {}
    for game in games:
        final_database[game] = build_game_questions(game)
    with open(input_file, "w", encoding="utf-8") as f:
        json.dump(final_database, f, indent=2)

if __name__ == "__main__":
    run_reconstruction()
    print("POLISHED DATABASE RECONSTRUCTION COMPLETE")
