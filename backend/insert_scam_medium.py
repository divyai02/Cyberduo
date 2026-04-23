# gitleaks:allow
from dotenv import load_dotenv
import os
load_dotenv('backend/.env')
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGO_URI'))
col = client['cyberduo']['questions']

col.delete_many({'game_key': {'$in': ['scam', 'scams']}, 'level_name': 'medium'})

questions = [
    # Q1 — adaptive_inbox (Support Triage)
    {
        "local_id": 1, "format": "adaptive_inbox", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Bulk Technical Support Scam Triage",
        "hint": "Phishers use 'Swipe' style tactics to catch you off guard. Look for 'Remote Access' requests and 'Expired Account' threats. Real companies don't DM you for support.",
        "explain": "Support scammers often use DMs or pop-ups. In this swipe triage, you must identify which messages are legitimate and which are fraudulent.",
        "reveal": "Triage Result: Microsoft Official (SAFE because it was a standard system update notification), Tech-Help-99 (PHISH - requested AnyDesk), Apple-Alert (PHISH - used a gmail address).",
        "questionText": "Triage Required! Your support inbox is full of urgent requests. Swipe through and mark them SAFE or PHISH!",
        "emails": [
            {"id": "e1", "subject": "Windows Update Available", "sender": "Microsoft (System Profile)", "isPhish": False},
            {"id": "e2", "subject": "CRITICAL: Install AnyDesk Now", "sender": "Tech-Support-Pro-99", "isPhish": True},
            {"id": "e3", "subject": "Your iCloud is full of VIRUSES!", "sender": "apple-support@gmail.com", "isPhish": True}
        ]
    },
    # Q2 — spot_fake (Romance Catfishing)
    {
        "local_id": 2, "format": "spot_fake", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Romance Scams (Catfishing)",
        "questionText": "Heart Trap! You meet 'Alex' on a dating app. After 2 days, Alex claims to be a soldier stuck abroad and needs $500 for a plane ticket to see you. One of these profiles is the scammer. Spot the fake!",
        "hint": "Scammers build trust, then have a 'Crisis' and need money. They often 'cannot video call' because of a broken camera or poor signal.",
        "explain": "Romance scams are long-term plays. Clues: relationship moves fast, they refuse to video call, and eventually request money via wire/crypto for an 'Emergency'.",
        "reveal": "SCAM! Three clues: 1) Model photos, 2) Refusal to video call, 3) Urgent request for $2,000 for a 'family emergency'. Block and report.",
        "brandName": "Dating App Profile - 'Alex'",
        "urlReal": "Verified Profile Status",
        "urlFake": "Unverified - No Video Proof",
        "options": [
            "It's a SCAM — impossible photos, no video calls, and a sudden money request",
            "It's LEGIT — people have emergencies"
        ],
        "correctAnswer": "It's a SCAM — impossible photos, no video calls, and a sudden money request"
    },

    # Q17 — spot_fake (Tech Support Pop-up)
    {
        "local_id": 17, "format": "spot_fake", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Technical Support — Browser Lock Pop-up",
        "questionText": "Emergency Alert! Your screen suddenly turns red with a loud siren and a message: 'Windows System Infected! Call 1-800-SAFE-NOW immediately.' Safe alert or SCAM?",
        "hint": "Pop-ups that say 'VIRUS DETECTED' and play a loud beep are trying to panic you. Real antivirus software is a separate app, not a browser tab.",
        "explain": "Browser lock scams use Javascript to disable the 'X' button and play alarm sounds. They ask you to call a Toll-Free number. If you call, they'll ask for $500 for a 'Fix'.",
        "reveal": "FAKE! The URL is 'secure-shield-alert-99.top'. Real Microsoft alerts never happen via a website window or ask you to call a random number.",
        "brandName": "Windows Defender",
        "urlReal": "System Settings > Windows Security",
        "urlFake": "http://secure-shield-alert-99.top/scan",
        "options": ["Legit System Alert", "Fake Browser Pop-up (SCAM)"],
        "correctAnswer": "Fake Browser Pop-up (SCAM)"
    },
    # Q18 — file_triage (Scam Invoice Triage)
    {
        "local_id": 18, "format": "file_triage", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Invoice Scams — The 'Overcharge' Lure",
        "hint": "Scammers send a fake invoice for $500 for a service you never bought (like 'Geek Squad'). They hope you'll call their number to 'cancel'.",
        "explain": "The 'Refund Scam' starts with a fake invoice. When you call to cancel, they tell you they 'accidentally' refunded you $5,000 and ask you to send the 'extra' $4,500 back via Bitcoin.",
        "reveal": "SUSPICIOUS: The 'Geek_Squad_Renewal.pdf' is the bait. If you didn't buy it, it's a scam. DELETE IT.",
        "files": [
            {"id": "inv1", "name": "Apple_Music_Receipt.pdf", "isMalware": False, "desc": "Matches your monthly subscription"},
            {"id": "inv2", "name": "Geek_Squad_Renewal_AutoPay_599.pdf", "isMalware": True, "desc": "Service you never subscribed to"}
        ]
    },
    # Q19 — sequence_builder (Reporting a Scam)
    {
        "local_id": 19, "format": "sequence_builder", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Incident Response — Reporting Procedure",
        "hint": "When you spot a scam: 1) NO CONTACT, 2) SCREENSHOT, 3) REPORT, 4) BLOCK.",
        "explain": "Never reply to a scammer; it just proves your number is active. Document the evidence, then use official platform reporting tools to protect others.",
        "reveal": "Correct Path: 1) Screenshot evidence, 2) Report to platform, 3) Block sender, 4) Delete thread. This stops the scammer and helps security teams find them.",
        "questionText": "Incident Response! You've identified a romance scammer. Arrange the steps to handle it safely:",
        "steps": [
            {"id": "s1", "text": "Take a Screenshot of the conversation", "correctOrder": 0},
            {"id": "s2", "text": "Report the profile to the platform", "correctOrder": 1},
            {"id": "s3", "text": "Block the scammer", "correctOrder": 2},
            {"id": "s4", "text": "Delete the message thread", "correctOrder": 3}
        ]
    },
    # Q20 — decision_simulator (QR Code Scams)
    {
        "local_id": 20, "format": "decision_simulator", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Quishing — Malicious QR Codes",
        "hint": "A QR code sticker on a public parking meter might be covering the real one. It sends your payment to a scammer's site instead of the city.",
        "explain": "QR Code Phishing (Quishing) is rising. Attackers place stickers over legitimate QR codes on menus, parking meters, or 'Pay Here' signs. Always check if the sticker looks peeling or 'added on'.",
        "reveal": "Decline! If a QR code directs you to a strange URL like 'pay-park-city-99.io' instead of the official city app, it's a scam to steal credit card data.",
        "questionText": "Parking Audit! A parking meter has a peeling sticker with a QR code saying 'Pay Faster via QR'. Scan result: 'pay-park-city-99.io'. Proceed?",
        "options": ["Scan and Pay — save time", "Decline — use the official machine coin/card slot", "Trust it if the logo looks real"],
        "correctAnswer": "Decline — use the official machine coin/card slot"
    },
    # Q21 — click_flags (Gift Card Scam Indicators)
    {
        "local_id": 21, "format": "click_flags", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Payment Methods — Why Gift Cards?",
        "hint": "Think: why would the IRS or Amazon need a Nike Gift Card? Because once you give them the code, the money is GONE and cannot be tracked.",
        "explain": "Gift cards are the currency of scammers. They are untraceable, non-refundable, and as good as cash. No legitimate company or government agency will ever ask for them as payment.",
        "reveal": "Flag the three red flags: 'Nike Gift Cards', 'Do not tell the clerk', and 'Urgent payment required'. These are the hallmarks of a retail scam.",
        "correctFlags": ["f1", "f2", "f3"],
        "questionText": "Retail Audit! A 'Police Officer' calls saying you have a warrant. 'Pay $500 in Nike Gift cards now or we're coming over.' Click the flags!",
        "emailParts": [
            {"id": "f1", "text": "Payment via Nike Gift Cards (RED FLAG)", "isFlag": True},
            {"id": "f2", "text": "Do not tell the store clerk what it's for (COERCION)", "isFlag": True},
            {"id": "f3", "text": "Immediate arrest if you hang up (PRESSURE)", "isFlag": True},
            {"id": "f4", "text": "Provide your badge number please. (NORMAL)", "isFlag": False}
        ]
    },
    # Q22 — scenario_mcq (Facebook Marketplace Zelle)
    {
        "local_id": 22, "format": "scenario_mcq", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Marketplace Scams — Overpayment Reversal",
        "hint": "The buyer 'accidentally' sends you $1,000 for a $100 item and asks you to 'send back the $900'. Their original $1,000 came from a hacked account and will be reversed later.",
        "explain": "The Overpayment scam is classic. You send your 'real' $900 back. Then the bank identifies the $1,000 as fraud and takes it out of your account. You lose $900 of your own money.",
        "reveal": "Do not send the money back yourself. Tell the buyer to resolve the 'accidental' transfer through Zelle/their bank directly. You are not responsible for their 'mistake'.",
        "questionText": "Sale Audit! A buyer sends you $500 for a $50 bike. 'Omg so sorry! My hands slipped. Can you Zelle me back the extra $450?' Your move?",
        "options": [
            "Zelle back the $450 — be a good person",
            "Keep the $500 — finders keepers",
            "Tell them to contact Zelle/Bank to reverse the transaction — do NOT send money yourself"
        ],
        "correctAnswer": "Tell them to contact Zelle/Bank to reverse the transaction — do NOT send money yourself"
    },
    # Q23 — adaptive_inbox (Social Media DM Triage)
    {
        "local_id": 23, "format": "adaptive_inbox", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Social Media — Malicious DM Triage",
        "hint": "DMs from 'old friends' saying 'I found this video of you' or asking for a '6-digit code' are scams after their account was hacked.",
        "explain": "When a friend's account is hijacked, the hacker sends DMs to all their contacts. 'Is this you? [LINK]' or 'I'm locked out, can you help me get back in with a code?' are traps to steal YOUR account next.",
        "reveal": "SAFE: Mom asking 'What's for dinner?'. PHISH: Old classmate saying 'OMG is this you in this video?' with a link, or 'Help me get back into my account, just send me the code you receive!'.",
        "questionText": "DM Triage! Your inbox is blowing up with odd messages. Swipe FAST to protect your digital life!",
        "emails": [
            {"id": "m1", "subject": "Hey! Check out this video of you!", "sender": "HighSchool-Friend-99", "isPhish": True},
            {"id": "m2", "subject": "I have a business idea, call me.", "sender": "Mom", "isPhish": False},
            {"id": "m3", "subject": "Can you send me the code Google just sent you? I'm locked out!", "sender": "Cousin-Vinny", "isPhish": True}
        ]
    },
    # Q24 — spot_fake (The 'Official' Instagram Meta Verified)
    {
        "local_id": 24, "format": "spot_fake", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Fake Ad Verification",
        "hint": "Check the spelling. 'Meta-Veri-fied' or 'Get-Badge-Now.net' are not official Meta properties. Real verification is done INSIDE the official app settings.",
        "explain": "Scammers buy ads that look like official system updates. 'Click here to keep your blue checkmark' leads to a fake login page. Meta never asks for your password via a website ad to 'verify' you.",
        "reveal": "FAKE! The URL is 'get-instabge-safe.io'. Official verification links never use hyphenated 'Get' domains. Stick to settings > account center.",
        "brandName": "Instagram Verified",
        "urlReal": "Internal App Settings",
        "urlFake": "http://get-instabge-safe.io/verify",
        "options": ["Official System Ad", "Imposter Phishing Ad"],
        "correctAnswer": "Imposter Phishing Ad"
    },

    # Q3 — deepfake_detection (Audio Mystery)
    {
        "local_id": 3, "format": "deepfake_detection", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "AI Voice Cloning",
        "hint": "AI clones often have unnatural pauses or lack emotion. If the request is for an 'Urgent Wire Transfer' outside of normal hours — verify!",
        "explain": "Voice deepfakes can be made from seconds of public audio. Scammers use this to call employees pretending to be the CEO and demand urgent transfers.",
        "reveal": "AI Deepfake! Clues: 1) Urgent wire request during a meeting, 2) Slightly robotic tone. Always verify via a separate, trusted channel.",
        "questionText": "Audio Audit! Voice note from CEO: 'Hey, I'm stuck in a board meeting. Wire $25,000 to this new vendor in NY immediately to secure the deal. Hurry!'",
        "options": ["Real CEO — Process the wire", "AI Voice Clone — Verify via Slack/Call first"],
        "correctAnswer": "AI Voice Clone — Verify via Slack/Call first"
    },

    # Q4 — scavenger_hunt (SIM Swap Clues)
    {
        "local_id": 4, "format": "scavenger_hunt", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "SIM Swapping Indicators",
        "hint": "The first sign is your phone suddenly losing ALL signal and saying 'No Service', while the internet still works on Wi-Fi.",
        "explain": "SIM swapping allows scammers to move your number to their SIM. They can then reset your banking and email passwords using SMS codes.",
        "reveal": "Click 'No Service' and 'Password Reset'! These are the smoking guns of a SIM swap. Call your provider immediately from another phone.",
        "correctAnswer": "Click: 'No Service' and the unexpected 'Email Password Reset'",
        "questionText": "Account Alert! Your phone is on Wi-Fi, but something is wrong with your cellular connection and mail. Find the two signs of a SIM SWAP!",
        "objects": [
            {"id": "o1", "icon": "📶", "label": "Status: No Service (Was 5G a minute ago!)", "isRedFlag": True, "top": "10%", "left": "10%"},
            {"id": "o2", "icon": "📧", "label": "Notification: Your Google Password was just reset (NOT BY YOU)", "isRedFlag": True, "top": "35%", "left": "55%"},
            {"id": "o3", "icon": "🌐", "label": "Wi-Fi: Connected (Safe)", "isFlag": False, "top": "60%", "left": "30%"},
            {"id": "o4", "icon": "🔋", "label": "Battery: 85% (Normal)", "isFlag": False, "top": "80%", "left": "70%"}
        ]
    },

    # Q5 — scenario_mcq (Pump and Dump)
    {
        "local_id": 5, "format": "scenario_mcq", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Crypto Scams — Pump and Dump",
        "hint": "A 'Pump and Dump' involves scammers hyping a worthless coin to drive the price up, then selling all their coins, crashing it to zero.",
        "explain": "In 'Rug Pulls', creators disappear with money. Signs: anonymous developers, heavy influencer promotion with no tech details.",
        "reveal": "It is a Pump & Dump. No asset goes up 500% in an hour for no reason. Real projects have Whitepapers and known developers.",
        "questionText": "Crypto Audit! You see a coin 'SafeMoonTurbo' up 500% in 2 hours. Influencers say 'To the moon! Buy now!' What is the most likely truth?",
        "options": [
            "It is a 'Moon Mission' — get rich with low risk",
            "It is a 'Pump and Dump' — you are being lured in to be the 'Exit Liquidity'",
            "Revolutionary technology everyone just discovered"
        ],
        "correctAnswer": "It is a 'Pump and Dump' — you are being lured in to be the 'Exit Liquidity'"
    },

    # Q6 — click_flags (Fake Marketplace Safety)
    {
        "local_id": 6, "format": "click_flags", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Marketplace Scams — Forced Off-Platform payment",
        "hint": "Scammers always want you to pay 'Off-Platform' (via Friends & Family, Venmo, or Gift Cards) because these have zero buyer protection.",
        "explain": "Legit marketplaces (eBay, Facebook) have built-in payment systems. Scammers say 'to avoid fees, pay me via Venmo'. Once you pay, the seller disappears and you can't get a refund.",
        "reveal": "Flag the 'Friends & Family' and 'Venmo' mentions! A legit seller won't force you off the platform's secure payment system. If they ask for payment as a 'Friend', they are removing your legal right to a refund.",
        "correctFlags": ["p1", "p2"],
        "questionText": "Marketplace Audit! You are buying a PS5 on Facebook. The seller says: 'Pay me via Venmo Friends & Family to avoid fees. I'll ship it today!' Click the red flags!",
        "emailParts": [
            {"id": "p1", "text": "Pay via Venmo Friends & Family (NO PROTECTION)", "isFlag": True},
            {"id": "p2", "text": "Avoid platform fees (COMMON EXCUSE)", "isFlag": True},
            {"id": "p3", "text": "I will provide a tracking number after shipping. (NORMAL)", "isFlag": False}
        ]
    },

    # Q7 — scenario_mcq (The Ponzi Scheme)
    {
        "local_id": 7, "format": "scenario_mcq", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Investment Scams — Ponzi Schemes",
        "hint": "A Ponzi scheme pays early investors using money from new investors. It inevitably crashes when they run out of new people to recruit.",
        "explain": "Classic signs: 'Guaranteed' high returns (e.g. 10% monthly) with 'No Risk'. Legitimate investments always have risk and market fluctuations.",
        "reveal": "It is a Ponzi Scheme. 'Guaranteed 1% daily' is mathematically impossible for real investments. The money you see in your 'Account' is just numbers on a screen; it doesn't really exist.",
        "questionText": "Wealth Audit! Your cousin joins 'Global-Wealth-Pro'. It guarantees 1% profit EVERY DAY with zero risk. You get extra money for 'Recruiting' friends. What is this?",
        "options": [
            "A high-frequency trading bot — very advanced technology",
            "A Ponzi / Pyramid Scheme — unsustainable and destined to crash",
            "A revolutionary new bank"
        ],
        "correctAnswer": "A Ponzi / Pyramid Scheme — unsustainable and destined to crash"
    },

    # Q8 — branching_narratives (The Grandparent Scam)
    {
        "local_id": 8, "format": "branching_narratives", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Social Engineering — Family Emergency (Impersonation)",
        "hint": "The scammer calls an elderly person pretending to be their grandchild: 'Hi Grandma, it's me. I'm in trouble and need help. Don't tell my parents!'",
        "explain": "This uses high emotion and 'Secrecy' to stop the victim from thinking. They claim they are in jail or a hospital abroad. The solution: hang up and call the grandchild's REAL number directly to verify.",
        "reveal": "Hang up and call the real number! Scammers use urgency and shame ('Don't tell my parents') to isolate victims. Verifying via a known secondary channel always breaks the scam.",
        "questionText": "Emergency Call! A caller says: 'Grandma, I'm in jail in Mexico. I need $5,000 for bail immediately. The lawyer said not to tell Dad because he'll be mad. Please help me!' What should Grandma do?",
        "options": [
            "Go to the bank immediately — her grandson is in danger",
            "Hang up and call her grandson's real phone number or his parents directly to verify",
            "Ask the caller for his social security number to verify identity"
        ],
        "correctAnswer": "Hang up and call her grandson's real phone number or his parents directly to verify"
    },

    # Q9 — click_flags (Employment Scam clues)
    {
        "local_id": 9, "format": "click_flags", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Job Scams — The 'Check' system",
        "hint": "A 'Job' that pays $50/hour for 'Remote Data Entry' and sends you a check to 'Buy your own equipment' is a scam. The check will bounce after you've sent real money to their 'vendor'.",
        "explain": "The 'Overpayment' or 'Equipment' check scam is common. The check they send is fake, but your bank makes the funds available for 24 hours. You send your 'Real' money to the scammer's 'Vendor'. 3 days later, the bank realizes the check is fake and takes the $3,000 back from your account.",
        "reveal": "Flag the '$3,000 Check' and 'Our Approved Vendor'. Real companies buy and ship equipment to you, or have a formal reimbursement process. They NEVER ask you to pay a 'Third Party' using your own bank account.",
        "correctFlags": ["p1", "p2"],
        "questionText": "Job Audit! You got a remote job offer. 'We are sending you a $3,000 check. Deposit it and use it to buy a laptop from Our Approved Vendor.' Click the red flags!",
        "emailParts": [
            {"id": "p1", "text": "Sending you a $3,000 check to deposit (FAKE FUNDS)", "isFlag": True},
            {"id": "p2", "text": "Buy from 'Our Approved Vendor' (SCAMMER ACCOUNT)", "isFlag": True},
            {"id": "p3", "text": "Interview was conducted over LinkedIn. (NORMAL-ish)", "isFlag": False}
        ]
    },

    # Q10 — link_inspector (The Fake Login Shield)
    {
        "local_id": 10, "format": "link_inspector", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Typosquatting in Scams",
        "hint": "Check the URL. 'pay-pal-security-support.com' is NOT paypal.com. Scammers use hyphens and extra words to look official.",
        "explain": "A real company like PayPal will always use their main domain. Hyphenated domains are cheap to buy and used for phishing redirects.",
        "reveal": "PHISHING SCAM! Destination 'pay-pal-security-dispute-resolution.net' is a fake. Real PayPal is always just paypal.com.",
        "displayedLink": "[ 🛡️ PAYPAL DISPUTE CENTER ]",
        "actualDestination": "https://pay-pal-security-dispute-resolution.net/auth",
        "correctAnswer": "Phishing",
        "questionText": "URL Forensic! An email says: 'Your PayPal account has a $500 dispute. Click here to review.' Hover over the 'Dispute Center' button. Safe or Scam?"
    },

    # Q11 — decision_simulator (The SIM Card Scam)
    {
        "local_id": 11, "format": "decision_simulator", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Physical Scams — The 'Street Survey' SIM swap",
        "hint": "A 'Street Promoter' asks to see your phone to 'Check your data speed' or 'Verify your account'. They are actually reading your ICCID (SIM ID) to clone it.",
        "explain": "Never hand your unlocked phone to a stranger on the street, even if they have a 'Uniform'. In seconds, they can scan your SIM details or install a hidden tracking app.",
        "reveal": "Decline and keep your phone! A legitimate mobile company will never ask to physically touch your phone on a sidewalk to 'verify your account'. They would do that via their official app or in a retail store.",
        "questionText": "Street Trap! A man in a 'Cyber-Mobile' vest says: 'We are doing a network speed test for customers. Can I just see your phone for 1 minute to check your SIM serial number?'",
        "options": [
            "Let him check — he has a professional vest and badge",
            "Decline — never hand your phone to a stranger to 'read' your SIM data",
            "Ask him to show you his speed test results first"
        ],
        "correctAnswer": "Decline — never hand your phone to a stranger to 'read' your SIM data"
    },

    # Q12 — scenario_mcq (Utility Scam — The 'Cut-off' threat)
    {
        "local_id": 12, "format": "scenario_mcq", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Utility Scams — High Pressure / Urgency",
        "hint": "Scammers call saying your 'Electricity will be cut off in 30 minutes' unless you pay via a Bitcoin ATM or Prepaid Gift Card immediately.",
        "explain": "Real utility companies give weeks of written notice before a disconnection. They will NEVER ask for payment via Bitcoin or Gift Cards. These are untraceable and non-refundable.",
        "reveal": "It is a SCAM. High pressure ('30 minutes') and unusual payment methods (Bitcoin) are the 100% confirmation. Hang up and call the number on your actual physical bill.",
        "questionText": "Utility Alert! You get a call from 'The Electric Co': 'Your payment is 2 months late. If you don't pay $300 via the Bitcoin ATM at the corner store in 1 hour, we are cutting your power!'",
        "options": [
            "Hurry to the ATM — you don't want to lose power",
            "It's a SCAM — utilities don't use Bitcoin or give 1-hour verbal warnings",
            "Ask for a discount if you pay in cash"
        ],
        "correctAnswer": "It's a SCAM — utilities don't use Bitcoin or give 1-hour verbal warnings"
    },

    # Q13 — click_flags (The 'Free Money' Government Grant)
    {
        "local_id": 13, "format": "click_flags", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Government Grant Scams — Processing Fees",
        "hint": "You've been selected for a '$5,000 Govt Grant' you didn't apply for. All you need to do is pay a '$50 Processing Fee' via Amazon Gift Card. See the trap?",
        "explain": "Legitimate government grants are hard to get and won't involve a 'Gift Card fee'. The scammer just wants your $50 (and likely your SSN during 'registration').",
        "reveal": "Flag '$50 Processing Fee' and 'Pay via Amazon Gift Card'. No government agency accepts gift cards for fees. If you didn't apply for a grant, you aren't 'Selected' for one.",
        "correctFlags": ["p1", "p2"],
        "questionText": "Grant Audit! An official looking 'Govt-Grant-Dept' message says you've won $5,000. 'Just pay the $50 fee using a gift card to release the funds.' Click the flags!",
        "emailParts": [
            {"id": "p1", "text": "$50 processing fee (THE REAL SCAM)", "isFlag": True},
            {"id": "p2", "text": "Pay using an Amazon Gift Card (UNTRACEABLE)", "isFlag": True},
            {"id": "p3", "text": "Provide your bank name for direct deposit. (NORMAL-ish risk)", "isFlag": False}
        ]
    },

    # Q14 — branching_narratives (The 'Accidental' Zelle Transfer)
    {
        "local_id": 14, "format": "branching_narratives", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Payment Platform Scams — Zelle / CashApp 'Accident'",
        "hint": "A stranger 'accidentally' sends you $500 on Zelle and asks you to 'Send it back'. The $500 they sent is from a hacked account; when that hack is caught, the bank takes the $500 back, but your 'send back' was a NEW real transfer.",
        "explain": "This is a money laundering / theft trick. Never send the money 'Back' directly. Tell the person to contact Zelle/Bank support to reverse it. If you send it yourself, you are out $500 once the original fraud is reversed.",
        "reveal": "Tell them to contact their bank! Never send money back to a stranger who claims they 'made a mistake'. Let the platform handle the reversal, or you will lose your own money when the original fake transfer is clawed back.",
        "questionText": "Payment Error! Someone sends you $400 on Zelle and DMs you: 'Omg sorry! That was for my rent. Can you please send it back to me? I made a typo in the phone number!' What do you do?",
        "options": [
            "Send it back — it's the right thing to do and they need it for rent",
            "Tell them to contact their bank for a reversal and do NOT send any money yourself",
            "Keep the money — it's your lucky day"
        ],
        "correctAnswer": "Tell them to contact their bank for a reversal and do NOT send any money yourself"
    },

    # Q15 — digital_whodunnit (Social Media Imposter)
    {
        "local_id": 15, "format": "digital_whodunnit", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Imposter Identification via Profile/Header data",
        "hint": "Check the verification status and history. A real Meta Support profile will not have 'Account Created Yesterday' and '0 Followers'.",
        "explain": "Social media imposters create 'Help' pages to trick you into giving up credentials. Check the 'Header' data of the profile to verify legitimacy.",
        "reveal": "The Imposter is 'support-security-updates-71'! It has NO verification badge and was created 2 hours ago. Real platform support comes through official system menus, not random follower-less profiles.",
        "correctAnswer": "support-security-updates-71",
        "questionText": "Whodunnit! Three profiles claim to be 'Meta Support' regarding a copyright strike. Use the forensic evidence table to select the imposter!",
        "emails": [
            {"id": "p1", "from": "Meta Verified Support", "spf": "PASS", "dkim": "PASS", "isImposter": False},
            {"id": "p2", "from": "support-security-updates-71", "spf": "FAIL", "dkim": "FAIL", "isImposter": True},
            {"id": "p3", "from": "Meta Business Help", "spf": "PASS", "dkim": "PASS", "isImposter": False}
        ]
    },

    # Q16 — select_all (Signs of a Prize Scam)
    {
        "local_id": 16, "format": "select_all", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Prize/Sweepstakes Scams",
        "hint": "Select ALL the signs that 'You won a free cruise!' is a scam. Think about why they need your credit card for a 'free' prize.",
        "explain": "If you have to pay to receive a 'free' prize, it isn't free. Scams demand: shipping fees, taxes, or 'verification' fees. They also use extreme urgency to stop you from checking your records for whether you even entered.",
        "reveal": "Flag all 4! 🚢 A prize you didn't enter, ⏳ 'Act in 5 minutes!', 💳 Request for card for 'Shipping', and 📧 Sent from a Gmail/Yahoo address. Legit companies don't use personal email accounts for prizes or charge 'Shipping' via gift cards.",
        "correctAnswer": "Select all 4: Urgency, Payment required for 'free', Didn't enter, Sent from personal email",
        "questionText": "Sweepstakes Sentry! You 'Won' a free trip to Hawaii. Select ALL the indicators below that prove it is a SCAM:",
        "options": [
            "You never actually entered a contest for a Hawaii trip",
            "The email says 'Offer expires in 120 seconds! Click now!'",
            "They need your credit card to pay a $25 'Customs Port Fee' for the free trip",
            "The email came from 'hawaii-trips-official@gmail.com'",
            "The email mentions your first name correctly"
        ],
        "correctFlags": [
            "You never actually entered a contest for a Hawaii trip",
            "The email says 'Offer expires in 120 seconds! Click now!'",
            "They need your credit card to pay a $25 'Customs Port Fee' for the free trip",
            "The email came from 'hawaii-trips-official@gmail.com'"
        ]
    },

    # Q25 — decision_simulator (The 'Wrong Number' Text)
    {
        "local_id": 25, "format": "decision_simulator", "difficulty": "medium",
        "gameName": "scam", "game_key": "scams", "level_name": "medium",
        "concept": "Pig Butchering / Wrong Number Scams",
        "hint": "A friendly text says: 'Hi Ben, are we still meeting for golf?' You aren't Ben. If you reply 'Wrong number', they start a long, friendly conversation to eventually lure you into a crypto scam.",
        "explain": "This is 'Pig Butchering'. They 'fatten' you up with weeks of friendship and then 'slaughter' you by steerng you to a fake investment app. The best move is to NEVER reply to a 'Wrong Number' text from a stranger.",
        "reveal": "Ignore and Delete! Replying 'Sorry, wrong number' confirms your phone number is 'Active' to the scammer's database. This will lead to even more spam and is the first step in a long-term psychological scam.",
        "questionText": "Stranger Danger! You get a text: 'Hey Sarah, the reservation is at 7pm tonight. Looking forward to it!' You aren't Sarah. What do you do?",
        "options": [
            "Reply 'Sorry, you have the wrong number' out of politeness",
            "Ignore and Delete the message immediately — it's likely a scam starter",
            "Call the number to let them know so they don't miss their dinner"
        ],
        "correctAnswer": "Ignore and Delete the message immediately — it's likely a scam starter"
    }
]

# Note: Final script will contain exactly 25.
# Ensure game_key is consistently 'scams'
for q in questions:
    q['game_key'] = 'scams'

result = col.insert_many(questions)
print(f"Inserted {len(result.inserted_ids)} unique Scam Medium missions.")
client.close()
