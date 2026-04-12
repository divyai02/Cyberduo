from dotenv import load_dotenv
import os
load_dotenv()
from pymongo import MongoClient

client = MongoClient(os.getenv("MONGO_URI"))
db = client["cyberduo"]
col = db["questions"]

# First ensure it's empty
col.delete_many({"game_key": "phishing", "level_name": "beginner"})

questions = [
    # Q1 — adaptive_inbox (Phish or Real? #1)
    {
        "local_id": 1,
        "format": "adaptive_inbox",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Recognising Phishing Emails",
        "hint": "Check who actually SENT the email — not just what it says in the subject line.",
        "explain": "Phishing emails pretend to be from trusted brands, banks or colleagues. The most reliable giveaway is always the sender's real email address. Legitimate companies always email from their own official domain.",
        "reveal": "✅ Correct! 'security@bankofamerica-alerts.xyz' is NOT a real Bank of America address. Real banks only contact you through their official domain (e.g. @bankofamerica.com). The '.xyz' domain is a major red flag!",
        "questionText": "🌅 Monday morning. Sort your inbox — swipe SAFE or flag as PHISH for each email!",
        "emails": [
            {"id": "e1", "subject": "Your Amazon order #3421 has shipped! 📦", "sender": "shipping@amazon.com", "isPhish": False},
            {"id": "e2", "subject": "URGENT: Your bank account has been locked", "sender": "security@bankofamerica-alerts.xyz", "isPhish": True},
            {"id": "e3", "subject": "Team lunch agenda for Wednesday 🥗", "sender": "sarah@yourcompany.com", "isPhish": False}
        ]
    },

    # Q2 — link_inspector (Link Roulette #1)
    {
        "local_id": 2,
        "format": "link_inspector",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "URL Inspection",
        "hint": "Hover over the button to reveal the REAL destination URL — read it carefully!",
        "explain": "A link button can display friendly text like 'Log in to PayPal' while secretly routing you to a completely different, dangerous website. Always hover to see the true URL before clicking anything.",
        "reveal": "⚠️ Phishing! The button says 'PayPal Login' but the real URL was 'paypal-secure-login.fakesite.net' — a copycat page designed to steal your password. Real PayPal links always start with paypal.com.",
        "questionText": "🎰 Link Roulette! An email has a button: 'Log in to PayPal'. Hover over it — where does it REALLY go?",
        "displayedLink": "Log in to PayPal →",
        "actualDestination": "http://paypal-secure-login.fakesite.net/account",
        "correctAnswer": "Phishing"
    },

    # Q3 — click_flags (Red Flag Scavenger Hunt #1)
    {
        "local_id": 3,
        "format": "click_flags",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Email Red Flags",
        "hint": "Check the sender's email address AND look carefully for any spelling mistakes in the email body.",
        "explain": "Every phishing email leaves clues! Attackers often use fake domains that look similar to real ones, and they frequently make spelling mistakes because they work fast. Train your eye to spot these signs instantly.",
        "reveal": "🎯 Nice catch! 'support@netflix.co.xyz' is NOT Netflix's real domain, and 'Verify Mmebership' is a telltale typo. Real Netflix emails only come from @netflix.com and are spell-checked.",
        "questionText": "🔍 Red Flag Hunt! This email claims to be from Netflix. Click ALL the suspicious parts to complete the mission!",
        "emailParts": [
            {"id": "p1", "text": "From: support@netflix.co.xyz", "isFlag": True},
            {"id": "p2", "text": "Subject: Action Required — Your Account", "isFlag": False},
            {"id": "p3", "text": "Dear Valued Customer,", "isFlag": False},
            {"id": "p4", "text": "Please click here to Verify Mmebership →", "isFlag": True},
            {"id": "p5", "text": "Netflix Support Team", "isFlag": False}
        ],
        "correctFlags": ["p1", "p4"]
    },

    # Q4 — deepfake_detection (CEO Whisperer #1)
    {
        "local_id": 4,
        "format": "deepfake_detection",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "AI Voice & Deepfake Scams",
        "hint": "Would your real CEO ever ask you to buy gift cards in secret? That request alone is a massive red flag!",
        "explain": "Scammers can now clone a person's voice using AI in minutes. They call employees pretending to be the CEO or boss and create a fake emergency. This is called 'vishing' and it's becoming more common every year.",
        "reveal": "🤖 Deepfake! Real executives NEVER ask employees to buy gift cards urgently and secretly. The robotic tone and unusual request are two of the biggest signs this was an AI-faked voice. Always verify with a callback!",
        "questionText": "🎙️ CEO Whisperer! You receive a voice note — read the transcript and decide: Real boss or AI deepfake?",
        "audioTranscript": "Hey, it's me the CEO. I'm trapped in a meeting and need a big favour ASAP. Buy ten $50 Google Play gift cards from any store. Keep this between us — it's a surprise for the team. Send me the codes immediately!",
        "visualCues": ["Unusually urgent request", "Asks for gift cards (classic scam)", "Demands secrecy from colleagues"],
        "options": ["Real CEO Call", "Deepfake Scam"],
        "correctAnswer": "Deepfake Scam"
    },

    # Q5 — build_phish (Lure Lab #1)
    {
        "local_id": 5,
        "format": "build_phish",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Anatomy of a Phishing Email",
        "hint": "Think like a hacker: which combination would make someone panic and act fast without thinking?",
        "explain": "Phishing works by combining a trusted identity (like your bank) with a scary, urgent message. By building a fake email yourself, you understand exactly how the psychology works — and you'll recognise it for life!",
        "reveal": "🧪 Lab success! Combining an official-looking brand identity with extreme urgency ('account closes in 24 hours!') is the exact formula attackers use to trick millions of people every day. Now you know the recipe!",
        "questionText": "🧪 Welcome to the Lure Lab! Build a convincing phishing email to understand how attackers think. Choose ONE lure and ONE urgency tactic:",
        "lures": [
            {"text": "🏦 Impersonate the victim's own bank", "correct": True},
            {"text": "📧 Send from a random Gmail address", "correct": False},
            {"text": "🛒 Pretend to be an unknown foreign shop", "correct": False}
        ],
        "urgencies": [
            {"text": "⚠️ 'Your account will be permanently closed in 24 hours!'", "correct": True},
            {"text": "📋 'We have updated our privacy policy.'", "correct": False},
            {"text": "🎉 'You have received a newsletter subscription!'", "correct": False}
        ]
    },

    # Q6 — inbox_triage (Grandma's Inbox #1)
    {
        "local_id": 6,
        "format": "inbox_triage",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Spotting Scam Emails",
        "hint": "Real family emails come from people Grandma knows. Be suspicious of unexpected prizes or warnings!",
        "explain": "Scammers frequently target older or less tech-savvy users with 'You won!' messages or fake computer warnings. These are almost always lies designed to scare or excite the reader into clicking something dangerous.",
        "reveal": "💝 Well done! 'winprize@sweepstakes.xyz' is a scam — Grandma never entered any contest! Real prize emails always come from official, verifiable domains. The family photo email from daughter.mary@gmail.com is obviously safe.",
        "questionText": "👵 Grandma called — her inbox is a mess! Help her sort which emails are safe to keep and which to DELETE as junk.",
        "emails": [
            {"id": "e1", "subject": "Photos from our Paris trip! 📸 Love you Mum!", "sender": "daughter.mary@gmail.com", "isPhish": False},
            {"id": "e2", "subject": "🎉 YOU WON $5,000! Claim your prize NOW before it expires!", "sender": "winprize@sweepstakes-global.xyz", "isPhish": True},
            {"id": "e3", "subject": "Your prescription is ready for pickup", "sender": "pharmacy@cvshealthcare.com", "isPhish": False}
        ]
    },

    # Q7 — spot_the_difference (Spot the Clone #1)
    {
        "local_id": 7,
        "format": "spot_the_difference",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Clone / Lookalike Websites",
        "hint": "Compare the two URLs character by character — one tiny letter change is hiding in plain sight!",
        "explain": "Attackers copy popular websites pixel-for-pixel. The ONLY reliable way to detect them is to check the URL (web address) in your browser bar. Always look before you type in any passwords!",
        "reveal": "🔎 Sharp eyes! The fake site used 'googIe.com' — that's a capital letter 'I' (eye) replacing a lowercase 'l' (ell). From a distance they look identical. This trick is called a homograph attack.",
        "questionText": "🔬 Spot the Clone! Two Google login pages look identical. Compare the URLs and find the tell-tale sign of the FAKE one!",
        "brandName": "Google",
        "urlReal": "accounts.google.com",
        "urlFake": "accounts.googIe.com",
        "options": ["The URL domain name", "The page logo size", "The Sign In button colour"],
        "correctAnswer": "The URL domain name"
    },

    # Q8 — branching_narratives (Urgency Pressure Cooker #1)
    {
        "local_id": 8,
        "format": "branching_narratives",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Social Engineering & Urgency",
        "hint": "Real emergencies at work still require proper process. When pressure is extreme — SLOW DOWN.",
        "explain": "Scammers deliberately create panic so you react without thinking. A real manager will always understand a brief delay for verification. If someone absolutely insists you skip all normal checks, they are almost certainly trying to trick you.",
        "reveal": "✅ Perfect call! Verifying directly with your manager by phone is always the right move. If it was a scam, you just saved the company thousands. If it was real, a good manager will appreciate your caution!",
        "questionText": "🔥 Pressure Cooker! Your 'manager' texts: 'URGENT! Transfer £2,000 to this new vendor immediately or we lose the contract! Do NOT wait!' What do you do?",
        "options": [
            "Transfer the money immediately — you can't afford to lose the deal!",
            "Ignore the message and hope someone else handles it.",
            "Stop. Call your manager directly on their known phone number to verify the request."
        ],
        "correctAnswer": "Stop. Call your manager directly on their known phone number to verify the request."
    },

    # Q9 — quishing_drills (Catch the Quish #1)
    {
        "local_id": 9,
        "format": "quishing_drills",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "QR Code Phishing (Quishing)",
        "hint": "Always read the actual URL a QR code leads to BEFORE you open it. Does it match the official site?",
        "explain": "Quishing is phishing via QR codes. Attackers print fake QR stickers and stick them on office notice boards, restaurant menus, or parking meters. Scanning them takes you to fake login pages designed to steal your information.",
        "reveal": "⚠️ Phishing! 'free-wifi-login.xyz' is NOT a real office WiFi portal. Real corporate WiFi networks use the company's own official domain. Attackers place these stickers to steal employee login credentials!",
        "questionText": "📸 Catch the Quish! You see a flashy poster in the office break room: 'Scan for FREE faster WiFi!' You scan it and see this URL. Safe or dangerous?",
        "qrObject": "Break Room WiFi Poster",
        "decodedURL": "http://free-wifi-login.xyz/office-access",
        "correctAnswer": "Phishing",
        "options": ["Safe", "Phishing"]
    },

    # Q10 — escape_rooms (Phish Tank Escape Room #1)
    {
        "local_id": 10,
        "format": "escape_rooms",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Cybersecurity Vocabulary",
        "hint": "The word means tricking PEOPLE (not computers) using trust, fear or fake authority. 4 letters: S _ _ _.",
        "explain": "In cybersecurity, 'Social Engineering' means convincing a human to do something unsafe — like clicking a link, sharing a password, or wiring money — by pretending to be someone trustworthy. Phishing is one of the most common types.",
        "reveal": "🔓 You escaped! The answer is 'SPAM' — unsolicited bulk email that often includes phishing, malware, and scam content. It's one of the oldest tricks in the book, and it still works on millions of people!",
        "questionText": "🔐 Escape Room! Your computer is locked. Crack the clue to break free: 'Unwanted bulk email that clogs your inbox and hides phishing traps. 4-letter word: _ _ _ _'",
        "cipherText": "VSDP",
        "correctAnswer": "SPAM"
    },

    # Q11 — cyber_snakes_ladders (Too Good to Be True #1)
    {
        "local_id": 11,
        "format": "cyber_snakes_ladders",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Recognising Scam Promises",
        "hint": "Ask yourself: 'Did I enter any competition to win this?' If not — it's almost certainly a scam!",
        "explain": "The 'Too Good to Be True' rule is one of the most powerful scam detectors. Legitimate businesses do not randomly give away iPhones or cash prizes to strangers. These messages are designed to make you click without thinking.",
        "reveal": "🎣 Classic scam! Random prize emails are an 'Advance Fee Fraud' or lottery scam. They lure you in with a big prize, then ask for a small 'processing fee' to claim it. You lose the fee and get nothing.",
        "questionText": "🐍 You landed on a Phishing Pit! An email arrives: 'Congratulations! You have won a FREE iPhone 15 — click here to claim in 10 minutes!' What type of scam is this?",
        "scenario": "Subject: 🎉 You are our LUCKY WINNER! Claim your FREE iPhone 15 before the timer runs out!",
        "options": ["Advance Fee / Lottery Scam", "Genuine Apple Promotion", "Legitimate Customer Reward"],
        "correctAnswer": "Advance Fee / Lottery Scam"
    },

    # Q12 — scavenger_hunt (Social Media Snoop #1) — format maps to scavenger_hunt
    {
        "local_id": 12,
        "format": "scavenger_hunt",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Spear Phishing & OSINT",
        "hint": "A phisher looks for information to make their fake email sound personal and convincing. Which details would they steal?",
        "explain": "Spear phishing is targeted phishing where attackers research their victim on social media first. They use personal details — like your pet's name, where you work, or a recent trip — to make the scam email feel real and trustworthy.",
        "reveal": "🕵️ You found it! 'Pet: Biscuit 🐶' and 'Works at: TechCorp' are exactly the kind of details a spear phisher would use. Example attack: 'Hi [Name], we noticed your dog Biscuit is registered at our TechCorp vet clinic — please verify your account.'",
        "questionText": "🕵️ Social Media Snoop! You're looking at a mock public profile. Click the details a phisher would STEAL to craft a convincing personalised attack!",
        "objects": [
            {"id": "o1", "icon": "🐶", "label": "Pet: Biscuit", "isRedFlag": True, "top": "15%", "left": "10%"},
            {"id": "o2", "icon": "🏢", "label": "Works at: TechCorp", "isRedFlag": True, "top": "15%", "left": "55%"},
            {"id": "o3", "icon": "🎨", "label": "Hobbies: Painting", "isRedFlag": False, "top": "55%", "left": "10%"},
            {"id": "o4", "icon": "📍", "label": "City: Manchester", "isRedFlag": False, "top": "55%", "left": "55%"}
        ]
    },

    # Q13 — adaptive_inbox (Phish or Real? #2 — different scenario: HR/IT emails)
    {
        "local_id": 13,
        "format": "adaptive_inbox",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Internal Phishing Disguises",
        "hint": "IT departments NEVER ask for your password via email. That's a hard rule!",
        "explain": "Attackers often pretend to be your own IT department or HR team because you're more likely to trust internal-sounding messages. Remember: legitimate IT staff will never ask for your password by email — ever.",
        "reveal": "✅ Got it! 'it.helpdesk@yourcompany-support.net' is NOT your internal IT team — the '.net' external domain gives it away. Real IT requests come from internal company addresses like @yourcompany.com.",
        "questionText": "📬 New emails have landed! Sort them fast — which one is the phishing trap hiding as an internal message?",
        "emails": [
            {"id": "e1", "subject": "Q2 payslips are now available in HR portal", "sender": "hr@yourcompany.com", "isPhish": False},
            {"id": "e2", "subject": "ACTION: Password expires in 1 hour — reset NOW", "sender": "it.helpdesk@yourcompany-support.net", "isPhish": True},
            {"id": "e3", "subject": "Fire drill this Thursday at 11am 🔔", "sender": "facilities@yourcompany.com", "isPhish": False}
        ]
    },

    # Q14 — link_inspector (Link Roulette #2 — different: fake Microsoft link)
    {
        "local_id": 14,
        "format": "link_inspector",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Fake Login Page Links",
        "hint": "Hover to reveal the real URL. Does the domain match microsoft.com exactly?",
        "explain": "Phishers create convincing Microsoft login pages on completely different domains. They then send links with descriptive anchor text so the URL is hidden until you hover. Always hover BEFORE you click any email link.",
        "reveal": "🚫 Phishing! The real URL 'microsofft-signin.com' has a double 'f' — a classic typosquatting trick. Microsoft's real login page is always at login.microsoftonline.com or account.microsoft.com.",
        "questionText": "🎰 Link Roulette Round 2! An email says 'Your Microsoft account needs attention'. Hover over the 'Verify Account' button — is the real link safe?",
        "displayedLink": "Verify Your Microsoft Account →",
        "actualDestination": "http://microsofft-signin.com/verify-account",
        "correctAnswer": "Phishing"
    },

    # Q15 — the_imposter (The Report Race — find the real phish in Slack messages)
    {
        "local_id": 15,
        "format": "the_imposter",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Business Messaging Scams",
        "hint": "Which message is asking you to do something unusual or give something away? That's your imposter!",
        "explain": "Attackers compromise or fake messaging accounts on Slack, Teams or WhatsApp to send believable phishing messages to colleagues. Unusual requests — especially involving money, gift cards, or urgent secrecy — from colleagues should always be verified verbally.",
        "reveal": "🏆 Found the imposter! 'David (Finance)' asking you to click an invoice link from a Google Drive shortlink is highly suspicious. Real Finance teams send documents through official company systems, not random Drive links.",
        "questionText": "🏅 Report Race! One of these Slack messages from your team is a phishing attempt. Find the imposter FIRST to win the round!",
        "messages": [
            {"sender": "Emma (Design)", "text": "The new brand assets are shared in our company SharePoint. Let me know what you think! 😊", "isPhish": False},
            {"sender": "David (Finance)", "text": "URGENT: Please open this invoice immediately → bit.ly/inv-2024 — needs your approval today!", "isPhish": True},
            {"sender": "Chris (HR)", "text": "Don't forget — team building session is on Friday at 3pm in meeting room B!", "isPhish": False}
        ],
        "options": ["Emma (Design)", "David (Finance)", "Chris (HR)"],
        "correctAnswer": "David (Finance)"
    },

    # Q16 — click_flags (Red Flag Scavenger Hunt #2 — different: fake DHL email)
    {
        "local_id": 16,
        "format": "click_flags",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Package Delivery Scams",
        "hint": "Look at the sender address and the link text — delivery companies use their OWN domain, not free email services.",
        "explain": "Package delivery scams are among the most common phishing attacks worldwide. Attackers send fake 'your parcel is delayed' emails with links to steal your card details under the guise of 'paying a customs fee'.",
        "reveal": "📦 Well spotted! 'dhl-delivery@gmail.com' is obviously fake — DHL would never use Gmail. Also, 'Pay £1.45 customes fee!' contains a spelling error ('customes'). These are clear signs of a scam!",
        "questionText": "📦 Scavenger Hunt Round 2! This email claims to be from DHL about your parcel. Find ALL the red flags!",
        "emailParts": [
            {"id": "p1", "text": "From: dhl-delivery@gmail.com", "isFlag": True},
            {"id": "p2", "text": "Subject: Your parcel could not be delivered", "isFlag": False},
            {"id": "p3", "text": "Dear Customer, we attempted to deliver your package today.", "isFlag": False},
            {"id": "p4", "text": "Pay £1.45 customes fee to release your parcel →", "isFlag": True},
            {"id": "p5", "text": "DHL Express Delivery Services", "isFlag": False}
        ],
        "correctFlags": ["p1", "p4"]
    },

    # Q17 — deepfake_detection (CEO Whisperer #2 — but this time it's REAL)
    {
        "local_id": 17,
        "format": "deepfake_detection",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Distinguishing Real vs AI Voice",
        "hint": "Does the message contain an unusual financial request? Does it ask for secrecy? These are key red flags.",
        "explain": "Not every urgent call from your boss is fake. The difference lies in the REQUEST — real executives use proper channels for significant decisions, never pressuring employees to bypass procedures or keep things secret.",
        "reveal": "✅ This one was REAL! The CEO is asking you to join a scheduled call through normal business channels — no weird requests, no secrecy, no bypassing process. It's always the unusual REQUEST that exposes a deepfake.",
        "questionText": "🎙️ CEO Whisperer Round 2! Listen to this voice message transcript — this time, is it the REAL CEO or a deepfake?",
        "audioTranscript": "Hi team, it's James your CEO. Just a reminder about our Q3 strategy call scheduled for 2pm today on Teams. Please have your department update slides ready. See you then!",
        "visualCues": ["Normal business request", "References a pre-scheduled meeting", "No urgency or secrecy"],
        "options": ["Real CEO Call", "Deepfake Scam"],
        "correctAnswer": "Real CEO Call"
    },

    # Q18 — file_triage (Attachment Bomb Squad)
    {
        "local_id": 18,
        "format": "file_triage",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Dangerous Email Attachments",
        "hint": "Documents like PDFs and JPEGs are usually safe. But .exe files and macro-enabled Office files are potentially dangerous!",
        "explain": "The Attachment Bomb Squad! Not all email attachments are safe. Executable files (.exe) and macro-enabled Office files (.xlsm, .docm) can contain malware. Regular PDFs and image files from known senders are generally safe.",
        "reveal": "💣 Defused! 'Invoice_Final.exe' is obviously dangerous — no real invoice comes as a Windows executable! 'Report.xlsm' is a macro-enabled Excel file that can auto-run malicious code. The PDF and JPEG were safe.",
        "questionText": "💣 Attachment Bomb Squad! Your inbox has 4 attachments. Mark each one as SAFE or MALWARE before something explodes!",
        "files": [
            {"id": "f1", "icon": "📄", "name": "CompanyReport_Q2.pdf", "isMalware": False},
            {"id": "f2", "icon": "💀", "name": "Invoice_Final.exe", "isMalware": True},
            {"id": "f3", "icon": "🖼️", "name": "TeamPhoto2024.jpg", "isMalware": False},
            {"id": "f4", "icon": "💀", "name": "Budget_Report.xlsm", "isMalware": True}
        ]
    },

    # Q19 — build_phish (Lure Lab #2 — different scenario: colleague impersonation)
    {
        "local_id": 19,
        "format": "build_phish",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Spear Phishing Construction",
        "hint": "The most convincing phish uses a familiar person AND a believable work reason. Which combo feels most normal?",
        "explain": "Spear phishing targets a specific person using personalised details. By pretending to be a known colleague with a plausible work request, attackers make it very hard to spot the fake. Building one yourself shows you exactly how believable these can be!",
        "reveal": "🧪 Experiment complete! Impersonating a real colleague combined with a plausible document request ('Can you review this contract?') is the most dangerous combo — it feels completely normal. This is how targeted corporate attacks begin.",
        "questionText": "🧪 Lure Lab Round 2! This time build a targeted attack on a specific employee. Pick your best combination:",
        "lures": [
            {"text": "👤 Pretend to be their direct manager at work", "correct": True},
            {"text": "👽 Send from an unknown foreign contact", "correct": False},
            {"text": "🤖 Pretend to be a random robot account", "correct": False}
        ],
        "urgencies": [
            {"text": "📎 'I've attached the contract — can you review and sign by 5pm today?'", "correct": True},
            {"text": "🌙 'Would you like to join our newsletter about gardening?'", "correct": False},
            {"text": "📅 'Let me know your availability for next month sometime.'", "correct": False}
        ]
    },

    # Q20 — scenario_mcq (Emoji Code Breaker)
    {
        "local_id": 20,
        "format": "scenario_mcq",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Recognising Scam Patterns",
        "hint": "Decode each emoji one by one: 💰 = money/prize, 🔗 = link, ⚡ = urgency/fast. What scam are they describing?",
        "explain": "Scammers sometimes use very simple language (or even emoji) to communicate with potential victims, especially via text message or WhatsApp. Learning to recognise the PATTERN of a scam (free prize + urgent link) is more important than knowing every specific trick.",
        "reveal": "🎉 Decoded! '💰🔗⚡' = 'Free money, click this link, right now!' — that is the classic formula for a prize or lottery scam. Whenever you see those three ingredients together, it's almost certainly a phishing attempt.",
        "questionText": "🔡 Emoji Code Breaker! You receive a text with only emojis: '💰🎁 FREE! Click 🔗 NOW! ⚡ Expires in 10 mins!' Decode this message — what type of scam is it?",
        "options": [
            "Lottery / Prize Phishing Scam",
            "A genuine competition notification",
            "A normal promotional marketing email"
        ],
        "correctAnswer": "Lottery / Prize Phishing Scam"
    },

    # Q21 — spot_the_difference (Spot the Clone #2 — Apple login page)
    {
        "local_id": 21,
        "format": "spot_the_difference",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "URL Spoofing",
        "hint": "Focus only on the web address (URL). Look at every character — one is subtly wrong on the fake page.",
        "explain": "Attackers clone Apple's login page perfectly because it's trusted globally. The only difference is always the URL. Fake Apple pages use domains like 'appie.com' or 'apple-id.com' — never the real appleid.apple.com.",
        "reveal": "🍎 Spotted! The fake site showed 'appIe.com' — with a capital 'I' (eye) instead of a lowercase 'l' (ell). They look identical in most fonts! Always copy-paste important URLs into a new tab rather than clicking email links.",
        "questionText": "🔬 Clone Detector! Two Apple ID login pages look completely identical. Which detail reveals the FAKE one?",
        "brandName": "Apple ID",
        "urlReal": "appleid.apple.com",
        "urlFake": "appleid.appIe.com",
        "options": ["The URL domain name", "The Apple logo colour", "The password field border"],
        "correctAnswer": "The URL domain name"
    },

    # Q22 — branching_narratives (Urgency Pressure Cooker #2 — HR scenario)
    {
        "local_id": 22,
        "format": "branching_narratives",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Phishing via Authority Figures",
        "hint": "HR departments have proper official portals for sensitive data. They never ask for it via a random email link.",
        "explain": "Attackers frequently impersonate HR because employees expect administrative requests from them and are used to providing personal information. Always access HR by going DIRECTLY to the official internal HR system, never via an email link.",
        "reveal": "✅ Excellent thinking! Typing the HR portal address directly into your browser is exactly the right approach. If the request was real, you'll find it there too. If not, you just avoided handing your data to a criminal.",
        "questionText": "📋 An email arrives from 'HR Department' saying: 'We need your personal banking details updated for payroll by TODAY — click the secure link below.' What should you do?",
        "options": [
            "Click the link and fill in your banking details — payroll is important!",
            "Reply to the email asking if it's real.",
            "Ignore the email and go directly to the official HR portal by typing its address yourself."
        ],
        "correctAnswer": "Ignore the email and go directly to the official HR portal by typing its address yourself."
    },

    # Q23 — quishing_drills (Catch the Quish #2 — restaurant menu QR)
    {
        "local_id": 23,
        "format": "quishing_drills",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "QR Code Safety in Public",
        "hint": "Does the URL match the restaurant's real name? Random hyphenated domains are a red flag!",
        "explain": "Attackers stick fake QR stickers over legitimate restaurant QR menus. When you scan, instead of seeing the menu, you're taken to a fake page that asks for your card details 'to view the menu'. Always check the URL after scanning!",
        "reveal": "🍕 Phishing detected! A real Italian restaurant would use their own website like 'pizzapalace.co.uk', not 'pizza-menu-order-now.xyz'. Attackers replace legitimate QR stickers with fake ones at busy restaurants!",
        "questionText": "🍕 You're at a restaurant. You scan the QR code on your table for the menu and see this URL. Is it safe to proceed?",
        "qrObject": "Restaurant Table Menu QR Code",
        "decodedURL": "http://pizza-menu-order-now.xyz/table12",
        "correctAnswer": "Phishing",
        "options": ["Safe", "Phishing"]
    },

    # Q24 — escape_rooms (Escape Room #2 — different word)
    {
        "local_id": 24,
        "format": "escape_rooms",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Phishing Terminology",
        "hint": "It rhymes with 'wishing'. It's the most common cyber attack in the world. 8 letters: P _ _ _ _ _ _ _.",
        "explain": "Phishing comes from the word 'fishing' — just like fishing with a hook and bait, attackers 'fish' for victims by dangling tempting or scary messages to lure them into revealing sensitive information. It's been the #1 cyber threat for over 20 years.",
        "reveal": "🎣 You escaped! 'PHISHING' — the act of tricking someone into revealing sensitive information (passwords, card numbers, etc.) through deceptive emails, texts or websites. You just decoded the name of the game!",
        "questionText": "🔐 Escape Room Round 2! Decode the encrypted word to unlock your system: 'The act of tricking people with fake emails and websites to steal their passwords. 8 letters: _ _ _ _ _ _ _ _'",
        "cipherText": "SKLVKLQJ",
        "correctAnswer": "PHISHING"
    },

    # Q25 — cyber_snakes_ladders (Too Good to Be True #2 — job offer scam)
    {
        "local_id": 25,
        "format": "cyber_snakes_ladders",
        "difficulty": "beginner",
        "gameName": "phishing",
        "game_key": "phishing",
        "level_name": "beginner",
        "concept": "Job Offer & Recruitment Scams",
        "hint": "Legitimate employers never pay employees in advance and never ask for payment. If they do — run!",
        "explain": "Fake job offer scams are increasing rapidly. Attackers post dream jobs on LinkedIn or send unsolicited emails, then ask for your personal details 'for onboarding' or even send a fake cheque and ask you to wire back a portion. Always verify job offers through the company's official website.",
        "reveal": "🚨 Scam! 'Work from home, earn $5,000/week, no experience needed, reply now' is a textbook job scam. Legitimate jobs don't promise unrealistic salaries, they don't demand urgency, and they have a proper application process with a real company.",
        "questionText": "🐍 Snake Alert! You receive an email: 'HIRING! Work from home — earn $5,000/week, no experience needed. Just reply with your bank details to get started!' What is this?",
        "scenario": "Subject: 🚀 Amazing job opportunity — Start TODAY, earn $5,000/week from home! No CV needed!",
        "options": ["A Fake Job / Recruitment Scam", "A Legitimate Remote Job Offer", "A Government Employment Scheme"],
        "correctAnswer": "A Fake Job / Recruitment Scam"
    }
]

result = col.insert_many(questions)
print(f"✅ Successfully inserted {len(result.inserted_ids)} phishing beginner questions into MongoDB!")
print("Question formats used:")
for i, q in enumerate(questions, 1):
    print(f"  Q{i:02d}: [{q['format']}] — {q['questionText'][:60]}...")

client.close()
