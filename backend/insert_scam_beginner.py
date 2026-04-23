import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv('backend/.env')
client = MongoClient(os.getenv('MONGO_URI'))
col = client['cyberduo']['questions']

# Clear any existing scam beginner questions
col.delete_many({'game_key': {'$in': ['scam', 'scams']}, 'level_name': 'beginner'})

questions = [

    # Q1 — decision_simulator (Sense of Urgency Freeze)
    {
        "local_id": 1, "format": "decision_simulator", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Urgency = Scam Red Flag",
        "hint": "The more urgent and panicked a message feels, the MORE suspicious you should be — not less. Real account problems do not disappear in 10 seconds. Scams do!",
        "explain": "Extreme urgency ('10 seconds!', 'RIGHT NOW!', 'IMMEDIATELY!') is the #1 psychological weapon used by all scammers. It is designed to bypass your thinking brain and force a panicked reaction. Real companies NEVER send countdown threats about deleting accounts. The golden rule: the more urgent a message feels, the slower and more careful you should act.",
        "reveal": "Stay calm and verify through the official website! Real services like banks, Amazon, and Google NEVER delete accounts via a panic countdown text. The correct action is to do nothing in response to the scary message, then separately open a new browser tab, type the official website address yourself, and log in normally to check your account. If nothing is wrong there, it was 100% a scam.",
        "questionText": "Urgency Freeze! A terrifying text pops up on your phone: 'YOUR ACCOUNT IS BEING DELETED IN 10 SECONDS! CLICK THE LINK BELOW RIGHT NOW OR LOSE EVERYTHING FOREVER!' What should you do?",
        "options": [
            "Click the link immediately to save your account — you cannot risk losing years of data",
            "Stay calm — do nothing in response to this message, then log into your account by typing the official website address yourself",
            "Forward the message to friends and family to warn them — the threat might be real for everyone"
        ],
        "correctAnswer": "Stay calm — do nothing in response to this message, then log into your account by typing the official website address yourself"
    },

    # Q2 — spot_fake (Hype Slide-Rule)
    {
        "local_id": 2, "format": "spot_fake", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Recognising Overhyped Money-Making Scam Ads",
        "hint": "Count the impossible promises. Real job opportunities pay realistic wages, require real skills, and never use countdown timers. If every line sounds too amazing — that is your answer!",
        "explain": "Every element of this ad is a scam signal. '$5,000 EVERY DAY' — unrealistic and unverifiable. 'No experience needed' — real skilled work pays for skills. '100% guaranteed success' — no investment can guarantee returns. 'ONLY 3 SPOTS LEFT' — fake scarcity. These are the exact psychological pressure tactics taught in scammer training manuals, designed to override your common sense with excitement.",
        "reveal": "SCAM STAMP! The formula is: impossible income + no effort required + 100% guarantee + fake limited spots + countdown pressure = guaranteed scam. Real work-from-home opportunities exist, but they pay realistic wages for defined tasks from registered companies with verifiable reviews. If an ad promises life-changing money for zero effort with a countdown, close it immediately and report it!",
        "questionText": "Hype Meter! Read this online ad and give it a Hype Score. Is it a legit opportunity or a SCAM worth stamping? The ad says: 'Make $5,000 EVERY DAY working from home! NO experience needed! NO skills required! 100% GUARANTEED results! Join 50,000 happy earners! ONLY 3 SPOTS LEFT — Register NOW before midnight!'",
        "options": [
            "LEGIT: A genuine work-from-home business opportunity worth investigating further",
            "SUSPICIOUS: Has a few warning signs but could be real — needs more research",
            "SCAM STAMP: Overflowing with impossible promises, fake urgency, and zero verifiable proof"
        ],
        "correctAnswer": "SCAM STAMP: Overflowing with impossible promises, fake urgency, and zero verifiable proof"
    },

    # Q3 — deepfake_detection (Deepfake Ear Test: AI cloned nephew)
    {
        "local_id": 3, "format": "deepfake_detection", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "AI Voice Cloning — Family Emergency Scam",
        "hint": "Real family members in genuine emergencies NEVER ask for gift card payments or demand you keep it secret from other family members. If you are unsure — hang up and call them directly on their saved number!",
        "explain": "AI can clone a person's voice from just 10-20 seconds of audio taken from social media. Scammers use this to call relatives pretending to be a family member in distress. Key red flags: refuses to video call, demands untraceable payment (gift cards / Cash App), insists on secrecy, and creates extreme urgency. Always verify by hanging up and calling the person on their REAL saved number.",
        "reveal": "AI Voice Scam! Every element is a red flag: the request for gift cards (untraceable and irreversible!), refusal to video call ('camera broken' — classic evasion), demands for secrecy from parents (isolates the target from other family members who might catch the scam), and a fake emergency designed to trigger panic generosity. Hang up immediately. Then call your nephew on the number you have saved for him. If he answers normally, you have confirmed the scam!",
        "questionText": "Ear Test! You receive a late-night call. The caller claims to be your nephew Chris and sounds emotional. Read the transcript — is this really Chris or an AI voice scam?",
        "audioTranscript": "Hi! It's me, Chris! Oh gosh, I'm so embarrassed. I was in a small accident and I'm at the police station. I need 1,500 pounds for bail RIGHT NOW. Please don't tell Mum and Dad — I don't want them to worry. Can you send it via gift cards or Cash App tonight? I'll pay you back first thing tomorrow, I promise. Please, I'm desperate!",
        "visualCues": [
            "Refuses to video call — 'my phone camera is broken'",
            "Requests untraceable gift card or Cash App payment only",
            "Urgently demands secrecy from other family members",
            "Voice sounds slightly robotic and unnatural under pressure"
        ],
        "options": ["Real Nephew Chris — Help Immediately", "AI Voice Scam — Hang Up and Call Chris Directly"],
        "correctAnswer": "AI Voice Scam — Hang Up and Call Chris Directly"
    },

    # Q4 — scavenger_hunt (Profile Scraper: What scammer steals from social media)
    {
        "local_id": 4, "format": "scavenger_hunt", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Social Media Oversharing and Scammer Data Mining",
        "hint": "Scammers look for personal details that answer typical security questions or prove identity. Pet names, schools, and birthdays are the magic three that unlock accounts and build believable fake emergencies!",
        "explain": "Scammers research their targets on social media before attacking — this is called OSINT (Open Source Intelligence). They look for: pet names (common security question: 'What is your pet's name?'), schools (common security question: 'What secondary school did you attend?'), and birthdays (used to verify identity when calling your bank pretending to be you). With these three, a scammer can reset your passwords, impersonate you, or craft a perfectly personalised phishing message about you!",
        "reveal": "The three items scammers steal: Pet name 'Coco' (answers 'What is your pet's name?' security question), High school 'Riverside High, Class of 2009' (answers school-based security questions), and Birthday 'Born: 14th June 1991' (used to pass bank identity verification). Favourite movie and emoji style are harmless — scammers cannot exploit these for account access or identity theft. Audit your own public profile and hide these three types of details!",
        "correctAnswer": "Click: Pet name, High school, and Birthday — all three answer security questions scammers use",
        "questionText": "Profile Scraper! A scammer is looking at this public social media profile to build a personalised attack. Click ALL the pieces of information they would STEAL to crack your accounts or impersonate you!",
        "objects": [
            {"id": "o1", "icon": "🐕", "label": "Pet: Coco the golden retriever 🐾", "isRedFlag": True, "top": "12%", "left": "8%"},
            {"id": "o2", "icon": "🏫", "label": "Education: Riverside High School, Class of 2009", "isRedFlag": True, "top": "12%", "left": "55%"},
            {"id": "o3", "icon": "🎂", "label": "Born: 14th June 1991", "isRedFlag": True, "top": "50%", "left": "8%"},
            {"id": "o4", "icon": "🎬", "label": "Favourite Movie: The Matrix", "isRedFlag": False, "top": "50%", "left": "55%"},
            {"id": "o5", "icon": "🌈", "label": "Vibe: Sunshine, coffee and good vibes 🌈☀️", "isRedFlag": False, "top": "80%", "left": "30%"}
        ]
    },

    # Q5 — link_inspector (Ghost URL #1: Amazon login fake button)
    {
        "local_id": 5, "format": "link_inspector", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Hidden Scam Links Behind Friendly Button Text",
        "hint": "Hover over the button to reveal where it REALLY goes. Look carefully — a zero '0' replacing the letter 'o', plus a '.ru' Russian domain instead of '.com', are massive red flags!",
        "explain": "This technique is called URL masking — the button displays friendly text ('Log in to Amazon') while secretly pointing to a completely different scam website. The real URL 'amaz0n-account-secure.ru' has two deliberate disguises: a zero (0) where there should be the letter 'o', and a Russian '.ru' domain. Amazon would never host their login page on a foreign domain like '.ru', '.xyz', or '.net'!",
        "reveal": "Phishing scam! The real URL was 'amaz0n-account-secure.ru' — not the real amazon.com. Two giveaways: '0' (zero) instead of 'o' in Amazon (typosquatting!), and a '.ru' Russian domain (Amazon's real login is only on amazon.com or amazon.co.uk). Entering your login details on this page would hand your username, password, saved address, and payment card to scammers instantly.",
        "questionText": "Ghost URL! An email has a big button saying 'Log in to Your Amazon Account'. Hover over it to reveal where the link REALLY goes. Is it safe or a scam?",
        "displayedLink": "Log in to Your Amazon Account →",
        "actualDestination": "http://amaz0n-account-secure.ru/login",
        "correctAnswer": "Phishing"
    },

    # Q6 — scenario_mcq (Too Good Price Tag: $10 laptop scam)
    {
        "local_id": 6, "format": "scenario_mcq", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Spotting Unrealistically Cheap Prices as Scam Bait",
        "hint": "A 98% discount from a seller with zero reviews is not a bargain — it is a trap. Real discounts from real sellers are usually 5–30% off, not 98% off. If the price makes you gasp, slow down!",
        "explain": "The '$10 laptop' scam works because our brains focus on the discount and not on the danger. The scammer takes your $10 payment, ships you nothing (or a broken brick in a box!), and then disappears. Scam platforms rely on people betting that the deal might just be real. Real bargains exist — but they come from established verified retailers with histories and reviews, not brand-new zero-review accounts selling luxury items for pennies.",
        "reveal": "The $10 price is the scam signal! No seller can profitably ship a $500 laptop for $10. When you see this price from a new seller with no reviews: you are about to lose $10, receive nothing of value, and have no recourse because the seller will vanish. Even if you think 'what have I got to lose at $10?' — these scams often collect card details that are then used for much larger charges. Real bargain rule: established verified retailers, rarely more than 40% off.",
        "questionText": "Price Tag Detective! You are shopping online for a brand-new laptop normally priced at $500. Three different sellers have listed it today. Which price is a SCAM RED FLAG?",
        "options": [
            "$499 — just $1 below the usual retail price from a seller with 4,200 positive reviews",
            "$425 — about 15% discount from a verified seller running a clearance sale",
            "$10 — 98% off the normal price, from a brand-new account created today with zero reviews"
        ],
        "correctAnswer": "$10 — 98% off the normal price, from a brand-new account created today with zero reviews"
    },

    # Q7 — branching_narratives (Marketplace Bait & Switch #1)
    {
        "local_id": 7, "format": "branching_narratives", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Staying Inside Official Marketplace Platforms for Safety",
        "hint": "Legitimate sellers WANT to stay on the official platform — it protects them too! The moment someone asks you to move off-platform, they are trying to escape the buyer protection that would catch them if they scam you.",
        "explain": "Moving transactions off official marketplace platforms (eBay, Amazon, Facebook Marketplace) to private messaging apps removes ALL buyer protection. eBay and PayPal have buyer guarantee programs — but only for purchases made entirely within their system. The 'bigger discount' offered outside is 100% fake — it is just the lure to get you somewhere unprotected where you are easy to scam with zero recourse.",
        "reveal": "Stay in the app! The 'move to WhatsApp for a bigger discount' trick is one of the most common online selling scams. Outside the platform you have no buyer protection, no dispute process, and no way to recover money if the seller disappears. Real trusted sellers never need to move to private apps — they are happy with the platform because it protects both parties. Report any seller who asks you to communicate or pay outside the official system!",
        "questionText": "Bait & Switch Alert! You found a great deal on eBay. The seller sends you a message: 'Let us move this to WhatsApp — I can give you a 20% bigger discount if we deal outside the app! Here is my number.' What should you do?",
        "options": [
            "Move to WhatsApp — an extra 20% discount sounds great and WhatsApp is just a messaging app",
            "Politely decline and insist the entire transaction stays within eBay's official platform",
            "Ask why they want to move first — if the reason sounds good, then move to WhatsApp"
        ],
        "correctAnswer": "Politely decline and insist the entire transaction stays within eBay's official platform"
    },

    # Q8 — click_flags (Charity Truth Serum: Find all red flags in fake charity appeal)
    {
        "local_id": 8, "format": "click_flags", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Identifying Fake Charity Appeals and Donation Scams",
        "hint": "Real registered charities have an official registration number, accept secure card or bank payments, use their own email domain, and never put a countdown timer on donations. Find all four red flags!",
        "explain": "Charity fraud spikes after every natural disaster because scammers know the public reacts emotionally and quickly. Warning signs: no charity registration number (all legitimate charities are registered with a government regulator), accepting only untraceable payment methods, fake 24-hour deadline urgency, and a personal Gmail address instead of an official organisation email. Always check the charity register before donating!",
        "reveal": "Four red flags found: No charity registration number (every legitimate charity has one — check your country's official charity register!), only Western Union and gift cards accepted (untraceable payment methods are always suspicious), 24-hour expiry deadline (fake urgency to stop you thinking!), and a personal Gmail contact email (real charities use @charityname.org or .com, not personal accounts). The cause statement itself is not suspicious — scammers wrap real-sounding causes around their fraud.",
        "correctAnswer": "Click the 4 red flags: no registration number, untraceable payment only, fake deadline, Gmail address",
        "questionText": "Charity Truth Serum! This charity appeal appeared on social media after a disaster. Find and click ALL the suspicious red flags that suggest this might be a fake charity collecting money for scammers!",
        "emailParts": [
            {"id": "p1", "text": "Charity Name: 'Kids Help Worldwide Foundation' — no charity registration number provided", "isFlag": True},
            {"id": "p2", "text": "Payment: ONLY accepts Western Union wire transfers or Amazon gift cards — NO credit card or PayPal", "isFlag": True},
            {"id": "p3", "text": "DONATE TODAY! This appeal EXPIRES in 24 HOURS — every cent goes straight to the children!", "isFlag": True},
            {"id": "p4", "text": "Contact us: helpkidsnow2024@gmail.com", "isFlag": True},
            {"id": "p5", "text": "Our cause: supporting children displaced by natural disasters in Southeast Asia", "isFlag": False}
        ],
        "correctFlags": ["p1", "p2", "p3", "p4"]
    },

    # Q9 — select_all (Gift Card Shredder: Why gift cards = always a scam)
    {
        "local_id": 9, "format": "select_all", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Gift Card Payment Scam Awareness",
        "hint": "No legitimate boss, government agency, IT department, or prize giver will EVER ask you to buy gift cards as payment. This is a universal, no-exceptions rule. Select ALL the reasons why!",
        "explain": "The 'Boss Gift Card Scam' (also CEO Fraud or Business Email Compromise) is devastatingly effective because it creates a believable authority scenario with urgency and secrecy. Once you share a gift card code, the money is gone instantly — codes work like cash and cannot be reversed. Companies NEVER buy awards, pay taxes, or settle debts with retail gift cards. This is 100% a scam format with zero exceptions.",
        "reveal": "All six are correct! The universal rule: NOBODY LEGITIMATE EVER ASKS FOR GIFT CARD CODES. Not your boss, not the IRS or HMRC, not Microsoft Support, not Google, not your electricity company, not Amazon. Gift cards are consumer retail tools — they have no role in business payments, government fees, or prize redemption. The moment anyone asks for gift card codes: stop, hang up, and call the supposed sender on their KNOWN number.",
        "correctAnswer": "All six reasons are correct — gift card requests are ALWAYS 100% a scam with no exceptions",
        "questionText": "Gift Card Shredder! A text arrives from your 'boss': 'Buy ten 100-pound Amazon gift cards for employee awards RIGHT NOW — I am in a meeting. Keep this confidential! Text me the codes immediately.' Select ALL the reasons this is definitely a scam:",
        "options": [
            "Legitimate companies NEVER purchase business expenses using retail gift card codes",
            "Real managers approve expenses through official company accounts, not personal texts",
            "Demanding secrecy ('keep this confidential') is a manipulation tactic used only by scammers",
            "Genuine urgent expenses have official approval paperwork — not just a hasty text message",
            "Gift card codes are untraceable and irreversible once shared — you cannot get the money back",
            "A real boss is always happy for you to call them on their known number to verify any unusual request"
        ],
        "correctFlags": [
            "Legitimate companies NEVER purchase business expenses using retail gift card codes",
            "Real managers approve expenses through official company accounts, not personal texts",
            "Demanding secrecy ('keep this confidential') is a manipulation tactic used only by scammers",
            "Genuine urgent expenses have official approval paperwork — not just a hasty text message",
            "Gift card codes are untraceable and irreversible once shared — you cannot get the money back",
            "A real boss is always happy for you to call them on their known number to verify any unusual request"
        ]
    },

    # Q10 — the_imposter (Secret Messenger: Find the fake friend asking for money)
    {
        "local_id": 10, "format": "the_imposter", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Identifying Fake Friend Money Request Scams",
        "hint": "The scam message combines three elements: a new or hacked account explanation, a fake emergency, AND an urgent request for untraceable money. Real friends in trouble call you first — they do not create new social media accounts and immediately ask for money!",
        "explain": "The 'friend hacked account' scam works by creating a believable story (old account was hacked, using a new one), adding a personal emergency (card blocked, stuck somewhere), and making the request feel private and urgent. Scammers compromise contact lists and target every person on it. Always verify money requests by calling your friend on their actual phone number — NOT by replying to the suspicious DM.",
        "reveal": "Jake_Real is the scammer! Three giveaways: 1) Claims this is a 'new account' because they were hacked — scammers say this to explain why the account looks unfamiliar, 2) Urgent request for £200 with a vague emergency and no verifiable details, 3) Claim that 'card is blocked' — this eliminates other payment options and points to bank transfers, which are hard to reverse. Real friends in trouble call you. Call the real Jake on his saved number before doing anything!",
        "questionText": "Secret Messenger! You receive DMs on Instagram from three people you know. One is a scammer pretending to be a friend to steal money. Find the IMPOSTER!",
        "messages": [
            {"sender": "Emma_M", "text": "Hey! Did I leave my scarf at yours last week? The green one with the stripes! Going through all my stuff now 😅", "isPhish": False},
            {"sender": "Jake_Real", "text": "Hi! I have been hacked — someone has my old account. This is my NEW account now. I am in a bad situation and need £200 urgently. My card is blocked and I cannot access funds. Can you help? I will pay back tomorrow!", "isPhish": True},
            {"sender": "Priya_S", "text": "Just uploaded the photos from Saturday to our group album — there are some great ones of us all! Check the shared folder 😊", "isPhish": False}
        ],
        "options": ["Emma_M", "Jake_Real", "Priya_S"],
        "correctAnswer": "Jake_Real"
    },

    # Q11 — sequence_builder (Verify a Suspicious Online Seller — correct steps in order)
    {
        "local_id": 11, "format": "sequence_builder", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Safe Online Marketplace Buying Process",
        "hint": "Start with the fastest and most powerful check — seller reviews. Then research further, confirm details, use protected payment, and keep a paper trail. Each step protects the next one!",
        "explain": "Safe online shopping follows a clear verification chain. Seller reviews are free and take 30 seconds — a new account with 0 reviews is an instant red flag. Googling the seller name reveals known scammers quickly. Confirming item details catches bait-and-switch attempts. Official platform payments include buyer protection. Keeping records provides evidence if you need to file a dispute later.",
        "reveal": "Correct verification order: 1) Check seller profile, reviews and account age (fastest red flag check!), 2) Google the seller name and product for known scam reports, 3) Verify item details match — photos, description, serial number, 4) Pay only through the official marketplace payment system, 5) Keep all messages and receipts inside the platform in case of dispute. This sequence protects you at every stage and builds a paper trail for recovery if something goes wrong!",
        "questionText": "Seller Verification! You found an amazing deal from an unknown seller online. Arrange these 5 safety steps in the CORRECT ORDER before handing over your money:",
        "steps": [
            {"id": "s1", "text": "Check the seller's profile age, review count and star rating — new accounts with zero reviews are high risk", "correctOrder": 0},
            {"id": "s2", "text": "Search the seller's name and product name on Google to check if others have reported them as a scam", "correctOrder": 1},
            {"id": "s3", "text": "Confirm the item details, photos, condition, and description match exactly what is advertised", "correctOrder": 2},
            {"id": "s4", "text": "Pay only through the official marketplace payment system — never by external bank transfer or gift cards", "correctOrder": 3},
            {"id": "s5", "text": "Keep all communication inside the marketplace app to have evidence if you need to file a dispute", "correctOrder": 4}
        ]
    },

    # Q12 — spot_fake (Tech Support Pop-up Panic)
    {
        "local_id": 12, "format": "spot_fake", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Fake Tech Support Scareware Pop-up Alerts",
        "hint": "This pop-up is just a scary webpage — it is NOT a real security alert. Real viruses are not detected by websites! The only safe exit is to force-close the entire browser without clicking ANYTHING shown in the pop-up.",
        "explain": "Scareware pop-ups are fake virus alerts displayed as webpages. They CANNOT actually scan your computer — they are designed to look like real alerts to trick you into panicking. Clicking 'Clean Now' downloads actual malware. Calling the number connects you to scammers (often called 'tech support scammers') who charge hundreds to 'fix' a problem that does not exist. The only correct response: force-close the browser without touching anything inside the pop-up.",
        "reveal": "Task Manager is the correct safe exit! Real antivirus software runs quietly in the background — it NEVER displays screaming full-screen pop-ups demanding phone calls or button clicks. No website can actually scan your hard drive for viruses. If you cannot close the tab normally, press Ctrl+Alt+Del (Windows) or force-quit (Mac) to close the browser entirely. Then run your REAL installed antivirus for peace of mind.",
        "questionText": "Pop-up Panic! Your browser suddenly fills with flashing red alerts: 'CRITICAL ALERT! YOUR PC IS INFECTED WITH 58 VIRUSES! CALL TECH SUPPORT NOW: 0800-FIX-SCAM OR CLICK CLEAN NOW IMMEDIATELY!' Which is the ONLY safe and correct response?",
        "options": [
            "Call the support number — speaking to a real person sounds safer than clicking buttons on screen",
            "Click 'CLEAN NOW' to remove the 58 viruses before they spread further to your files",
            "Force-close the browser using Windows Task Manager (Ctrl+Alt+Del) without clicking anything inside the pop-up",
            "Type your email into the pop-up to receive free virus removal instructions from their team"
        ],
        "correctAnswer": "Force-close the browser using Windows Task Manager (Ctrl+Alt+Del) without clicking anything inside the pop-up"
    },

    # Q13 — scenario_mcq (Stranger Danger Map: Geographic Inconsistency Tells)
    {
        "local_id": 13, "format": "scenario_mcq", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Identifying Romance Scam Geographic Deception",
        "hint": "Time zones do not lie! Someone claiming to be in London but sending messages at 3-4AM London time is almost certainly not in London. Ask yourself: where in the world is it 8-9AM when it is 3-4AM in London?",
        "explain": "Geographic deception is a core romance scam technique. Scammers operate from countries far away but claim to be local to build closeness. They cannot meet in person (excuses: travel, overseas work, military posting), they have professional-looking photos (often stolen from real people's accounts), and their messages arrive at times completely inconsistent with their claimed location. Time zone mismatches are the most reliable and hardest to fake red flag.",
        "reveal": "Messages at 3-4AM local time is the strongest geographic red flag! A person genuinely in London would be asleep during those hours — but 3AM London time is 8AM in West Africa (Nigeria, Ghana), which is where many romance scammers operate. Compliments and fast attachment are suspicious but not impossible for real people. Professional photos are suspicious but could be from a real attractive person. The time zone inconsistency, however, is practically impossible to explain away legitimately!",
        "questionText": "Stranger Danger Map! You have been chatting with a new online friend named Alex who claims to live in your city (London). Something feels off. What is the biggest red flag worth noting?",
        "options": [
            "Alex sends lots of compliments and seems very romantically interested very quickly",
            "Alex's messages consistently arrive between 3AM and 4AM London time despite claiming to live in London",
            "Alex has only been on the platform for 6 weeks and has fewer than 20 connections",
            "Alex's profile photo looks professional like it might be from a modelling shoot"
        ],
        "correctAnswer": "Alex's messages consistently arrive between 3AM and 4AM London time despite claiming to live in London"
    },

    # Q14 — decision_simulator (Overpayment Math Puzzle: Reject or refund the cheque)
    {
        "local_id": 14, "format": "decision_simulator", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Recognising and Refusing Overpayment Scams",
        "hint": "Here is what always happens: the cheque is counterfeit and bounces 2-3 weeks later. But the money you transferred back is already gone — and YOU are liable. The bank takes YOUR real money back. Reject any overpayment from a stranger!",
        "explain": "The Overpayment Scam is one of the oldest and most successful online selling frauds. The cheque IS fake. Banks clear cheques quickly but do not always detect sophisticated forgeries immediately. The scammer gets you to transfer real cash before the fraud is detected. When the cheque bounces weeks later, the bank recovers it from your real account — but your transfer to the scammer is already gone and almost impossible to trace or recover.",
        "reveal": "Reject the payment entirely! The 'accidental' overpayment is never an accident — it is the setup. No genuine buyer accidentally writes a cheque for 10x the agreed price. The cheque will be counterfeit and will eventually bounce — after you have already sent the 'refund' of real money from your real account. You lose £1,800 and your sofa. Always insist on the exact correct amount through a verified payment method. If a buyer insists on overpaying, they are a scammer — end the transaction immediately!",
        "questionText": "Overpayment Maths Puzzle! You are selling a sofa online for £200. A buyer contacts you: 'I accidentally wrote my cheque for £2,000 instead of £200. Please bank it and transfer me back the £1,800 difference today — I will collect the sofa next week.' What is the correct response?",
        "options": [
            "Accept the cheque and transfer back the £1,800 — the buyer seems genuine and you keep your fair £200",
            "Reject the payment entirely — overpayment from a stranger is a near-certain scam setup",
            "Accept the cheque but wait a full month for it to completely clear before transferring anything back"
        ],
        "correctAnswer": "Reject the payment entirely — overpayment from a stranger is a near-certain scam setup"
    },

    # Q15 — scavenger_hunt (Official Logo Match: Find the fake government agency logo)
    {
        "local_id": 15, "format": "scavenger_hunt", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Detecting Fake Official Authority Logos in Scam Letters",
        "hint": "Real government logos are professionally designed, registered, and have been in use for decades. Any logo with a silly element, a brand-new or unrecognisable agency name, or missing an official government seal is suspicious. Does this agency actually exist?",
        "explain": "Scammers create fake government-looking logos to make their fraud letters look legitimate and scare victims into paying. Common tactics: invent a convincing authority-sounding name, use eagles, official-looking fonts, and government colours. But real agencies have verifiable logos on their official government websites. Always search the agency name online before responding to any letter that demands payment or personal information!",
        "reveal": "The FAKE is the 'National Tax Refund Processing Bureau' logo! Three giveaways: this agency does not exist in any real government directory (search it — nothing comes up!), the eagle is holding a pizza slice (absurd detail added carelessly), and 'Est. 2024' (no real government agency announces its founding year on a fraud letter). Real tax agencies are the IRS (US), HMRC (UK), CRA (Canada) — all easily verified online. Never pay or provide details based on a letter from an agency you cannot verify!",
        "correctAnswer": "Click: National Tax Refund Processing Bureau — fake agency, pizza eagle, brand-new founding date!",
        "questionText": "Logo Shredder! Five official-looking government logos appear on letters. One is FAKE — created by a scammer to look authoritative. Find the fake logo and shred it before it tricks someone!",
        "objects": [
            {"id": "o1", "icon": "🏛️", "label": "IRS — Internal Revenue Service: Official black eagle seal, 'Department of the Treasury'", "isRedFlag": False, "top": "10%", "left": "5%"},
            {"id": "o2", "icon": "👑", "label": "HMRC — Her Majesty's Revenue and Customs: Official UK Government crown logo", "isRedFlag": False, "top": "10%", "left": "55%"},
            {"id": "o3", "icon": "🍕", "label": "National Tax Refund Processing Bureau: Eagle holding a pizza slice. Est. 2024. No official seal.", "isRedFlag": True, "top": "48%", "left": "5%"},
            {"id": "o4", "icon": "🏛️", "label": "FBI — Federal Bureau of Investigation: Official seal with Latin motto, founded 1908", "isRedFlag": False, "top": "48%", "left": "55%"},
            {"id": "o5", "icon": "🌐", "label": "INTERPOL — International Criminal Police Organization: Official red and navy globe logo", "isRedFlag": False, "top": "80%", "left": "30%"}
        ]
    },

    # Q16 — link_inspector (Ghost URL #2: PayPal fake verify button)
    {
        "local_id": 16, "format": "link_inspector", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "URL Spoofing — Fake Secure Payment Page Links",
        "hint": "Hover to see the REAL destination. PayPal's real website is ONLY ever at paypal.com. Look for the subtle number '1' replacing the letter 'l' in paypa1 — and the wrong '.net' domain instead of '.com'!",
        "explain": "Typosquatting is when scammers register domain names that look almost identical to real websites by changing one character — 'paypa1.net' instead of 'paypal.com'. They combine this with URL masking (showing friendly button text to hide the real address) to trick people into entering their payment credentials on a fake page. PayPal email links should NEVER be clicked — always type paypal.com directly into your browser instead.",
        "reveal": "Phishing scam! Spot the two differences from real PayPal: 1) 'paypa1' has a number '1' where there should be a lowercase letter 'l' (look carefully — they appear nearly identical in some fonts!), and 2) the domain is '.net' instead of '.com'. PayPal's login page is ONLY at paypal.com — never .net, .org, .ru, or any other variation. Golden rule for payment sites: never click links in emails, always type paypal.com yourself into a fresh browser tab!",
        "questionText": "Ghost URL Round 2! An email says your PayPal account needs attention. There is a big button: 'Verify Your PayPal Account'. Hover over the button to reveal the REAL link — is it safe or a scam?",
        "displayedLink": "Verify Your PayPal Account →",
        "actualDestination": "http://paypa1-secure-login.net/verify-account",
        "correctAnswer": "Phishing"
    },

    # Q17 — file_triage (Sort scam vs real messages in your inbox)
    {
        "local_id": 17, "format": "file_triage", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Quickly Sorting Scam Messages from Real Notifications",
        "hint": "Real messages come from official verified domains and mention your specific account details. Scam messages use random numbers, suspicious domains (.xyz, .net for tax agencies), prize announcements, or ask for personal data by email or text.",
        "explain": "Scam texts and emails are designed to look like official notifications from trusted organisations. Key differences: real notifications come from official short codes or verified registered domains; real messages reference your actual known account details; fake ones have suspicious domains, urgency, prize announcements, or requests for personal data. HMRC (UK tax) and IRS (US tax) NEVER email or text you requesting your bank details — they always write formal letters.",
        "reveal": "SAFE: Barclays payment reminder (no action needed, references a real known payee) and Amazon dispatch email (from the real amazon.com domain). SCAM: ASDA prize text from a random phone number with a '.xyz' domain (ASDA contacts verified prize winners through official channels, never random numbers!) and the HMRC 'refund' email to a fake domain (real HMRC is only hmrc.gov.uk — and they NEVER email you to collect bank details!).",
        "correctAnswer": "SAFE: Barclays reminder, Amazon dispatch — SCAM: ASDA prize text, HMRC-lookalike refund email",
        "questionText": "Inbox Bomb Squad! Your phone just buzzed with 4 new messages. Sort each one — is it a genuine SAFE notification or a SCAM to delete immediately?",
        "files": [
            {"id": "f1", "icon": "🏦", "name": "Barclays Bank SMS: Your scheduled payment of £45.00 to Electric Co goes out tomorrow. No action needed.", "isMalware": False},
            {"id": "f2", "icon": "💀", "name": "Text from +447234556601: CONGRATS! You have been chosen for a FREE £500 ASDA voucher! Claim at: asda-prizes.xyz before midnight", "isMalware": True},
            {"id": "f3", "icon": "📦", "name": "Email from shipping@amazon.com: Your order #AB-99123 has been dispatched. Expected delivery: Friday.", "isMalware": False},
            {"id": "f4", "icon": "💀", "name": "Email from HMRC-Tax@govt-refund-service.net: Your £842 tax refund is ready. Provide your bank details HERE to receive funds today.", "isMalware": True}
        ]
    },

    # Q18 — deepfake_detection (CEO Voice Test Round 2: This one is REAL)
    {
        "local_id": 18, "format": "deepfake_detection", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Distinguishing Real Authority Calls from AI Voice Scams",
        "hint": "Real business calls reference actual scheduled events, make no unusual financial or secretive request, and have a clearly normal purpose. It is the NATURE of the request — not just the voice — that reveals a scam!",
        "explain": "Not every call from an authority figure is a scam — and over-reacting to all of them creates unnecessary panic. The difference between a real call and a deepfake scam is always in the REQUEST, not just who appears to be calling. Real executive calls reference real known events, ask for nothing unusual, and have zero financial or secrecy components. Scam calls always manufacture emergencies, demand unusual action, and require secrecy.",
        "reveal": "Real CEO Call! This is exactly what a legitimate business reminder sounds like. It references a real pre-scheduled quarterly event, asks only for standard department reports, has a calm unhurried tone, requires no secrecy, and involves no financial request of any kind. Compare this to the Round 1 call (nephew needing gift cards in secret urgently) — completely different pattern. Learning to distinguish helps you stay alert without being paranoid about every phone call from your boss!",
        "questionText": "Ear Test Round 2! You are an employee and receive a voicemail from your CEO James. Read the transcript carefully — is this your real CEO or another AI voice impersonation scam?",
        "audioTranscript": "Hi team, it is James here — just a quick reminder that our quarterly strategy review is this Thursday at 2PM in the main boardroom on floor 4. Please bring your department progress reports as usual. Nothing else — just wanted to make sure everyone is confirmed for Thursday. Thanks everyone, see you then!",
        "visualCues": [
            "References a pre-existing scheduled quarterly meeting",
            "Normal calm tone — no urgency, pressure or emotional manipulation",
            "No financial request of any kind",
            "No demand for secrecy — openly mentions the whole team is invited"
        ],
        "options": ["Real CEO Call — Attend the Thursday Meeting", "AI Voice Scam — Report to IT Security Immediately"],
        "correctAnswer": "Real CEO Call — Attend the Thursday Meeting"
    },

    # Q19 — branching_narratives (Grandparent Verifier: What to do with the jail call)
    {
        "local_id": 19, "format": "branching_narratives", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Verifying Family Emergency Calls Before Sending Money",
        "hint": "The safest response to ANY urgent money call from family is always to hang up and call them directly on the phone number you already have saved. Scammers cannot intercept that call — and if your grandchild is genuinely fine, the mystery is solved in 30 seconds!",
        "explain": "The 'Grandparent Emergency Scam' specifically targets older people because scammers know grandparents react with immediate emotional generosity to grandchildren in distress. They use AI voice cloning (trained on social media posts), scripted emergencies, demands for secrecy, and untraceable payment methods. The single most effective defence: hang up and call the person directly on their already-saved number. This takes 30 seconds and cannot be faked or intercepted.",
        "reveal": "Call your grandchild directly! Hanging up and dialling the number you already have for them takes under a minute and is 100% definitive. If they answer normally ('Hi Gran, I'm great — why?') you have confirmed it was a scam. If they do not answer, call their parents or another family member immediately. Never send money based solely on one phone call without this verification, no matter how emotional, realistic, or urgent the call sounds. Scammers have perfected the emotional script.",
        "questionText": "Grandparent Verifier! You receive an emotional call: 'Gran, it is me! I was in an accident and I am at the police station abroad. I need 3,000 pounds for bail RIGHT NOW — please do not tell Mum, she will worry so much. Are you there?' What is the correct response?",
        "options": [
            "Send the 3,000 pounds immediately via wire transfer — you cannot risk your grandchild being in trouble",
            "Ask a secret question only your real grandchild would know the answer to, like your pet's name",
            "Hang up calmly, then call your grandchild directly on the phone number you already have saved for them"
        ],
        "correctAnswer": "Hang up calmly, then call your grandchild directly on the phone number you already have saved for them"
    },

    # Q20 — click_flags (Ad Red Flag Hunt: Work-from-home scam ad)
    {
        "local_id": 20, "format": "click_flags", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Spotting Every Red Flag in a Classic Work-From-Home Scam Ad",
        "hint": "Count the red flags: guaranteed huge income + no experience needed + fake limited spots + upfront registration fee + no verifiable company details = five red flags in one ad. Real jobs have NONE of these!",
        "explain": "Legitimate remote jobs exist — but they are never advertised with ALL of these elements together. Real job listings state realistic pay rates, do not have countdown timers, use real employee photos, NEVER charge you to start working, and are from registered companies with verifiable physical addresses and registration numbers. When every element of an ad screams too-good-to-be-true — it is!",
        "reveal": "All five are red flags! 1) '£500 GUARANTEED daily' — impossible for unskilled work (real remote jobs pay real-world wages!), 2) '2 spots left at midnight' — fake scarcity pressure designed to stop you researching, 3) Stock-photo testimonial — real reviews have verifiable real people, 4) £49 upfront registration fee — you should NEVER pay to start a job (employers pay employees, not the reverse!), 5) No company registration number or address — a legitimate business is always findable and contactable. Run from any ad with all five!",
        "correctAnswer": "Click all 5: guaranteed daily income, fake scarcity countdown, stock testimonial, upfront fee, no company details",
        "questionText": "Red Flag Hunt! This work-from-home advertisement appeared in your social media feed. Click ALL the parts that are WARNING SIGNS of a scam:",
        "emailParts": [
            {"id": "p1", "text": "Earn £500+ GUARANTEED every single day! No experience or qualifications needed whatsoever!", "isFlag": True},
            {"id": "p2", "text": "ONLY 2 SPOTS LEFT IN YOUR AREA — This offer closes at midnight tonight!", "isFlag": True},
            {"id": "p3", "text": "Testimonial: 'I made £10,000 in my very first week!' — Sarah T. *(stock photo, unverifiable)*", "isFlag": True},
            {"id": "p4", "text": "To reserve your guaranteed spot, pay a small £49 registration fee to unlock your starter kit", "isFlag": True},
            {"id": "p5", "text": "Company: WorkFromHome-UK Ltd (no registration number, no physical address listed anywhere)", "isFlag": True}
        ],
        "correctFlags": ["p1", "p2", "p3", "p4", "p5"]
    },

    # Q21 — the_imposter (Romance Scammer: Find the fake in a community chat group)
    {
        "local_id": 21, "format": "the_imposter", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Identifying Classic Romance Scam Profile Tactics",
        "hint": "The romance scammer's intro follows a very specific script: high-status profession, currently overseas (explains no in-person meeting), widowed with a child (generates maximum sympathy), and introduces romantic interest in the very FIRST message to a stranger.",
        "explain": "Romance scammers follow a documented playbook. The 'military officer/engineer/doctor posted overseas' profile is the single most common romance scam persona globally — it explains unavailability for video calls or meetings (operational security), generates admiration and trust (high status career), and creates a sympathy hook (widow, child needing a mother figure). Real community members introduce themselves normally — not romantically and with their entire tragic backstory in the first message!",
        "reveal": "Colonel_James_US is the scammer! Every element matches the documented romance scam template: military officer (credibly distant and admired), stationed overseas (cannot meet, cannot video call), widowed (maximum sympathy), young daughter (extra emotional attachment hook), and romantically signals intent in the very first message to strangers. Within a week of chatting, 'Colonel James' will manufacture a financial emergency — medical bills for his daughter, airline ticket home, or a stolen wallet. The script is the same every time. Block immediately and report the profile!",
        "questionText": "Romance Scam Radar! Three new people have joined your local community group and introduced themselves. One is running a classic romance scam. Find the IMPOSTER before they target a victim!",
        "messages": [
            {"sender": "Beth_London", "text": "Hello everyone! I am Beth, just moved to London last month for a new job. I love hiking and trying new restaurants — happy to be part of this community!", "isPhish": False},
            {"sender": "Colonel_James_US", "text": "Greetings, friends! I am Colonel James, a decorated US Army officer currently stationed overseas for 8 more months. I am widowed with a young daughter and I am looking for friendship and perhaps love. Would you be my friend? 🌹", "isPhish": True},
            {"sender": "David_K", "text": "Hey — David here! Software developer and massive football fan. Looking forward to talking Premier League with people in the area! ⚽️", "isPhish": False}
        ],
        "options": ["Beth_London", "Colonel_James_US", "David_K"],
        "correctAnswer": "Colonel_James_US"
    },

    # Q22 — select_all (Online Shopping Scam Warning Signs: multi-select all red flags)
    {
        "local_id": 22, "format": "select_all", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Recognising All Red Flags of a Fake Online Shopping Site",
        "hint": "Real brand websites use their own official domain, accept secure card payments with buyer protection, have realistic pricing, have verifiable business contact details, own their product photography, and have organic reviews built over time. Any site missing several of these is suspicious!",
        "explain": "Fake designer goods websites are extremely common. They steal real product images from official brand sites, create lookalike domain names, and set prices just low enough to seem like a sale. When you order: you either receive a terrible counterfeit or nothing at all. Payment by bank transfer or cryptocurrency makes money recovery virtually impossible. Three or more of these red flags together = close the tab immediately.",
        "reveal": "All six are genuine red flags of a scam shopping site! 1) Not the real brand domain (never trust a brand on a '.xyz', '.net' or hyphenated domain!), 2) No card or PayPal option (means no buyer protection if it goes wrong!), 3) Entire range 80% off (impossible to be profitable for a real retailer!), 4) Only a Gmail contact (no legitimate business uses Gmail as its main customer contact!), 5) Stolen product images (real retailers have their own photography!), 6) Identical 5-star reviews posted on the same day (fake review bombing — real reviews grow organically over time!). Three or more of these signals together is enough to leave!",
        "correctAnswer": "All six are genuine red flags — three or more together on one site means it is almost certainly a scam",
        "questionText": "Shopping Scam Detector! You found a website selling designer trainers at amazingly low prices. Select ALL the warning signs on this site that suggest it is a FAKE scam store:",
        "options": [
            "The website domain is 'nike-discount-official-sale.xyz' instead of the real nike.com",
            "The site only accepts bank transfer or cryptocurrency — no credit card, no PayPal available",
            "Every single item on the entire site is listed at exactly 80% below the normal retail price",
            "The 'Contact Us' page only has a Gmail address and no phone number or physical business address",
            "Product photos look identical to the official brand website's professional images",
            "Customer reviews are all 5 stars, posted on the same day, with very similar short generic text"
        ],
        "correctFlags": [
            "The website domain is 'nike-discount-official-sale.xyz' instead of the real nike.com",
            "The site only accepts bank transfer or cryptocurrency — no credit card, no PayPal available",
            "Every single item on the entire site is listed at exactly 80% below the normal retail price",
            "The 'Contact Us' page only has a Gmail address and no phone number or physical business address",
            "Product photos look identical to the official brand website's professional images",
            "Customer reviews are all 5 stars, posted on the same day, with very similar short generic text"
        ]
    },

    # Q23 — sequence_builder (Safely Donate to Charity: correct step-by-step verification)
    {
        "local_id": 23, "format": "sequence_builder", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Safe Step-by-Step Charity Donation Verification",
        "hint": "Start with the most powerful verification tool — the official government charity register. If a charity is not registered there, do not donate. Each step protects and confirms the next one!",
        "explain": "Charity fraud spikes after every major disaster because scammers know the public wants to help immediately. The verification chain protects your donation at every stage: the official register confirms legitimacy, checking the domain prevents lookalike site fraud, reviewing accounts shows efficiency, donating directly avoids phishing, and keeping a receipt creates a proof trail for your own records.",
        "reveal": "Correct safe order: 1) Check the official charity register (the fastest and most definitive legitimacy check!), 2) Verify the website domain matches the registered charity name (prevents lookalike website fraud), 3) Check published financial accounts to see how much of each donation reaches beneficiaries vs admin, 4) Donate directly through the official website — never via a link in an email or social media share, 5) Save your receipt with the charity registration number as proof. Following this chain means your generosity cannot be hijacked by scammers!",
        "questionText": "Charity Safety Chain! You want to donate to a charity after a major disaster. Put these 5 verification steps in the CORRECT ORDER to ensure your money reaches real people in need — not scammers!",
        "steps": [
            {"id": "s1", "text": "Search the charity name on your country's official charity register (e.g., Charity Commission UK or IRS database US)", "correctOrder": 0},
            {"id": "s2", "text": "Verify that the charity's website domain matches the registered organisation — check for lookalike copycat domains", "correctOrder": 1},
            {"id": "s3", "text": "Look up the charity's published financial accounts to check what percentage of donations actually reaches beneficiaries", "correctOrder": 2},
            {"id": "s4", "text": "Donate directly through the official website — never through a link forwarded in an email or social media message", "correctOrder": 3},
            {"id": "s5", "text": "Save your donation receipt which includes the charity registration number as personal proof for your records", "correctOrder": 4}
        ]
    },

    # Q24 — adaptive_inbox (Quick-sort scam vs real messages)
    {
        "local_id": 24, "format": "adaptive_inbox", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Rapid Safe vs Scam Message Classification",
        "hint": "Real notifications come from official verified domains and reference real accounts. Prize messages from random numbers with countdown timers, and 'official' messages using personal Gmail addresses, are always scams!",
        "explain": "Quick scam detection is a trainable skill. The fastest checks are: Does the sender domain match the real organisation? Does the message reference a specific real account action? Does it contain a prize, urgent payment, or request for personal details you did not initiate? Once you train your eye to spot these patterns, recognising scam messages takes just seconds.",
        "reveal": "SAFE: The Tesco Clubcard points update (from the real tesco.com domain, no action needed) and the bank statement alert (from the verified lloydsbank.com). SCAM: The Amazon 'prize' (from a win-now.xyz domain — nowhere near amazon.com — with a countdown, which Amazon never uses!) and the HMRC tax refund request (from a Gmail address — HMRC's real domain is hmrc.gov.uk and they NEVER ask for bank details by text or email!)",
        "questionText": "Inbox Flash Sort! Three new messages arrived. Swipe each one as SAFE to keep or SCAM to delete — decide fast before the timer runs out!",
        "emails": [
            {"id": "e1", "subject": "Your Tesco Clubcard points are ready to spend this month!", "sender": "clubcard@tesco.com", "isPhish": False},
            {"id": "e2", "subject": "You have WON a £500 Amazon Gift Card — CLAIM YOUR PRIZE IN 1 HOUR!", "sender": "amazon-rewards@win-now.xyz", "isPhish": True},
            {"id": "e3", "subject": "Your monthly bank statement is now available to view online", "sender": "statements@lloydsbank.com", "isPhish": False}
        ]
    },

    # Q25 — digital_whodunnit (Overpayment Scam Timeline: find the critical mistake)
    {
        "local_id": 25, "format": "digital_whodunnit", "difficulty": "beginner",
        "gameName": "scam", "game_key": "scams", "level_name": "beginner",
        "concept": "Tracing the Critical Moment in an Overpayment Scam",
        "hint": "The mistake happened BEFORE any money moved. The critical decision point was the moment Maria agreed to the overpayment arrangement — not the moment she transferred, not when the cheque appeared to clear!",
        "explain": "By Day 2 when the cheque appeared to 'clear', it was already too late. Banks show funds as available quickly but can take weeks to detect sophisticated counterfeit cheques. The 'cleared' balance was provisional credit, not confirmed real funds. The correct response at Day 1, 11AM was simply: 'I cannot accept that — please send exactly £150.' If the buyer refused, they were never a genuine buyer.",
        "reveal": "Day 1 at 11AM is the critical mistake moment! The instant the buyer mentioned an 'accidental overpayment' and asked for a refund transfer, every alarm should have triggered — because genuine buyers do not accidentally overpay by 10x. Countering with 'Please send exactly £150 and I will accept that' would have ended the scam instantly. The counterfeit cheque bounced weeks after the incident. The bank recovered £2,000 from Maria's real account (the provisional credit was reversed) — and her £1,800 transfer to the scammer was already gone, irretrievable. Maria lost £1,800 plus the sofa.",
        "questionText": "Scam Crime Scene! Maria sold her bicycle on Facebook Marketplace and got scammed. Read this timeline and identify the EXACT moment where Maria made the critical mistake that cost her £1,800:",
        "headers": [
            {"field": "Day 1 — 10:00 AM", "value": "Maria lists her bicycle for £200 on Facebook Marketplace. Buyer 'Tom' contacts her within minutes: 'I will take it — can I pay by personal cheque?'", "isSuspicious": False},
            {"field": "Day 1 — 11:00 AM", "value": "Tom says: 'I accidentally wrote the cheque for £2,000 instead of £200 — so sorry! Please bank it and transfer me back the £1,800 difference today. My online banking is broken right now.' Maria agrees.", "isSuspicious": True},
            {"field": "Day 2 — 09:00 AM", "value": "Maria deposits the cheque at her bank. Her banking app shows the full £2,000 has 'cleared' and appears in her available balance.", "isSuspicious": False},
            {"field": "Day 2 — 10:00 AM", "value": "Maria transfers £1,800 to Tom's account as agreed. Tom collects the bicycle with a friendly smile and never contacts Maria again.", "isSuspicious": True}
        ],
        "options": [
            "Day 1 at 10AM — Maria should never have listed the bicycle publicly online in the first place",
            "Day 1 at 11AM — Maria should have refused the overpayment and insisted on receiving exactly £200",
            "Day 2 at 9AM — Maria made a mistake by banking a cheque from a stranger at all",
            "Day 2 at 10AM — Maria should have waited at least 3 months before transferring any money back"
        ],
        "correctAnswer": "Day 1 at 11AM — Maria should have refused the overpayment and insisted on receiving exactly £200"
    }

]

# Ensure game_key is consistently 'scams'
for q in questions:
    q['game_key'] = 'scams'

result = col.insert_many(questions)
count = col.count_documents({'game_key': 'scam', 'level_name': 'beginner'})
print("Inserted: " + str(len(result.inserted_ids)) + " scam spotter beginner questions")
print("Total scam beginner questions in DB: " + str(count))
print("")
print("Format order (checking for consecutive duplicates):")
prev = ""
all_ok = True
for i, q in enumerate(questions):
    consecutive = " <<< CONSECUTIVE DUPLICATE!" if q['format'] == prev else ""
    if consecutive:
        all_ok = False
    print("  Q" + str(q['local_id']).rjust(2) + ": " + q['format'] + consecutive)
    prev = q['format']

print("")
print("Formats used per type:")
from collections import Counter
counts = Counter(q['format'] for q in questions)
for fmt, cnt in sorted(counts.items()):
    over = " <<< OVER LIMIT!" if cnt > 2 else ""
    print("  " + fmt + ": " + str(cnt) + over)

if all_ok:
    print("\nAll good -- no consecutive duplicate formats!")
else:
    print("\nWARNING: Consecutive duplicates detected!")

client.close()
