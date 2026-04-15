from dotenv import load_dotenv
import os
load_dotenv()
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGO_URI'))
col = client['cyberduo']['questions']

# Clear any existing password beginner questions first
col.delete_many({'game_key': 'password', 'level_name': 'beginner'})

questions = [

    # Q1 - password_triage (Drag & Drop Strength Bin #1)
    {
        "local_id": 1, "format": "password_triage", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Password Strength Basics",
        "hint": "A strong password is LONG, RANDOM, and uses a MIX of uppercase, lowercase, numbers AND symbols. Dragging a password to DELETE removes it from consideration.",
        "explain": "Passwords are rated by how long they take to crack. Sequential numbers like '12345678' fall in under a second. Names combined with birth years are guessable in minutes. A random mix of unrelated words with symbols can take millions of years! Only use the DELETE option if there is a clearly broken/empty entry.",
        "reveal": "Results: 12345678 = WEAK (sequential numbers, cracked instantly). jessica2003 = WEAK (real name + birth year, easily guessed). Blue-Tiger-99! = STRONG (random words + number + symbol = very hard to crack). There is nothing to delete here — all three are real passwords being classified!",
        "correctAnswer": "WEAK: 12345678, WEAK: jessica2003, STRONG: Blue-Tiger-99!",
        "questionText": "Strength Bin Challenge! Drag each password into the STRONG or WEAK bin. Judge based on length, randomness, and character variety:",
        "passwords": [
            {"id": "pw1", "text": "12345678", "isStrong": False},
            {"id": "pw2", "text": "Blue-Tiger-99!", "isStrong": True},
            {"id": "pw3", "text": "jessica2003", "isStrong": False}
        ]
    },

    # Q2 - scenario_mcq (Pass-Emoji Memory #1)
    {
        "local_id": 2, "format": "scenario_mcq", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Passphrase Memory Technique",
        "hint": "Think about WHY a funny story is easier to remember than a random string of characters!",
        "explain": "The emoji story technique teaches us to use passphrases — combining unrelated words into a mental image. 'DogPizzaRainbow' is 15 characters with no pattern, yet you can visualise it instantly. It is far stronger AND easier to remember than 'Ra!n8ow9'.",
        "reveal": "Correct! 'Dog + Pizza + Rainbow' creates the passphrase 'DogPizzaRainbow' — long, memorable, and unguessable. Combining random unrelated words into a story is one of the most powerful password techniques recommended by security experts!",
        "correctAnswer": "Combining random unrelated words into a story makes passwords long, strong AND memorable",
        "questionText": "Pass-Emoji Memory! You see this on a security poster: Dog + Pizza + Rainbow = DogPizzaRainbow password. What password principle does this emoji story teach?",
        "options": [
            "Emoji-only passwords are the most secure since hackers cannot type them",
            "Combining random unrelated words into a story makes passwords long, strong AND memorable",
            "Short passwords are safer as long as they contain an emoji or special image"
        ]
    },

    # Q3 - click_flags (Guess the Weakness #1)
    {
        "local_id": 3, "format": "click_flags", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Personal Information in Passwords",
        "hint": "Hackers start by guessing your first name, surname, and birth year — these are the FIRST things they try!",
        "explain": "Using your real name and birth year in a password is extremely dangerous. Hackers use social engineering — they look up your name and birthday on social media and try them first as possible passwords. Your personal info is NOT secret from a determined attacker!",
        "reveal": "The weak parts were: 'John' (first name), 'Smith' (surname), and '1990' (birth year). All three are publicly findable on social media or LinkedIn. The '!' symbol was the only thing adding any security — but it is not enough against a targeted attack.",
        "correctAnswer": "Click: John (first name), Smith (surname), 1990 (birth year) — all personal info!",
        "questionText": "Guess the Weakness! The password is: JohnSmith1990! — Click on ALL the parts that make it weak and easy for a hacker to guess:",
        "emailParts": [
            {"id": "p1", "text": "John", "isFlag": True},
            {"id": "p2", "text": "Smith", "isFlag": True},
            {"id": "p3", "text": "1990", "isFlag": True},
            {"id": "p4", "text": "!", "isFlag": False}
        ],
        "correctFlags": ["p1", "p2", "p3"]
    },

    # Q4 - cyber_snakes_ladders (Cracker Tug-of-War #1)
    {
        "local_id": 4, "format": "cyber_snakes_ladders", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Dictionary Attack Defence",
        "hint": "A Dictionary Attack tries real English words. What kind of password cannot be found in ANY dictionary?",
        "explain": "A Dictionary Attack is when a hacking tool automatically tries every word in the dictionary as your password — dragon, summer, sunshine, cookie, password. Words and predictable sequences appear on these lists. Random combinations of unrelated items do NOT and that is your best defence!",
        "reveal": "The correct patch is using a random mix not in any dictionary. 'Rocket!Lamp42&Sky' cannot be cracked by a dictionary attack because it is not a real phrase or word. Simply capitalising the first letter of a dictionary word offers almost no extra protection!",
        "questionText": "Cracker Tug-of-War! A hacker bot is attacking with a 'Dictionary Attack' — trying every English word as your password. Which defence patch stops it?",
        "scenario": "HACKER BOT ATTACK: Dictionary Attack in progress — testing: dragon, summer, sunshine, password, secret, cookie...",
        "options": [
            "Change 'dragon' to 'Dragon' — just capitalise the first letter",
            "Use a random mix of unrelated words + symbols + numbers NOT found in any dictionary (e.g. Rocket!Lamp42&Sky)",
            "Change your password once every single year"
        ],
        "correctAnswer": "Use a random mix of unrelated words + symbols + numbers NOT found in any dictionary (e.g. Rocket!Lamp42&Sky)"
    },

    # Q5 - password_builder (Passphrase Story Builder)
    {
        "local_id": 5, "format": "password_builder", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Building a Strong Passphrase",
        "hint": "Pick 4 random unrelated words that form a funny mental image. Avoid your name or birth year! Add a symbol or number to boost strength.",
        "explain": "A passphrase combines random unrelated words into a long, memorable sequence. 'BlueTiger!EatingPizza' is 20 characters with uppercase, lowercase, and a symbol — incredibly hard to crack yet easy to picture! Avoid using personal details like your own name or the current year.",
        "reveal": "Great passphrase choices! Words like Blue, Tiger, Eating, Pizza, and 99! work brilliantly together — random, unrelated, and memorable. Avoid 'John' (it's a personal name) and '2024' (it's the current year hackers always try). Aim for 12 or more characters total!",
        "correctAnswer": "Use random unrelated words + symbol/number pieces, avoid John (personal name) and 2024 (current year)",
        "questionText": "Passphrase Story Builder! Drag word pieces into the password box to build a strong, memorable passphrase. Watch the strength meter and aim for the highest score. Avoid the red-flagged pieces!",
        "pieces": [
            {"id": "w1", "text": "Blue", "type": "word", "isPersonalInfo": False},
            {"id": "w2", "text": "Tiger", "type": "word", "isPersonalInfo": False},
            {"id": "w3", "text": "Eating", "type": "word", "isPersonalInfo": False},
            {"id": "w4", "text": "Pizza", "type": "word", "isPersonalInfo": False},
            {"id": "w5", "text": "John", "type": "word", "isPersonalInfo": True},
            {"id": "w6", "text": "99!", "type": "symbol", "isPersonalInfo": False},
            {"id": "w7", "text": "2024", "type": "number", "isPersonalInfo": True},
            {"id": "w8", "text": "Ax#7", "type": "symbol", "isPersonalInfo": False}
        ]
    },

    # Q6 - adaptive_inbox (MFA Gatekeeper #1)
    {
        "local_id": 6, "format": "adaptive_inbox", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Multi-Factor Authentication (MFA)",
        "hint": "Real logins come from YOUR devices in YOUR location. Anything from a foreign country, at 3AM, or on an unknown device is suspicious and should be DENIED!",
        "explain": "MFA is a second lock on your account. Even if a hacker has your password, they still need to approve a login notification on your phone. Learning to approve genuine logins and deny suspicious ones is a critical security skill.",
        "reveal": "Correct! Logins from London on your own iPhone and office MacBook are clearly you — APPROVE. A login from North Korea at 3AM on an unknown Linux PC is definitely NOT you — DENY immediately and change your password!",
        "correctAnswer": "APPROVE: familiar city and your own devices. DENY: North Korea 3AM unknown Linux PC",
        "questionText": "MFA Gatekeeper! Three login requests are arriving on your phone. Tap APPROVE (🟢 SAFE) for logins that look like you, and DENY (🔴 PHISH) for suspicious ones:",
        "emails": [
            {"id": "r1", "subject": "New login — London UK (your home city)", "sender": "Device: Your iPhone, Safari Browser", "isPhish": False},
            {"id": "r2", "subject": "New login — North Korea at 3:00 AM", "sender": "Device: Unknown Linux PC, never seen before", "isPhish": True},
            {"id": "r3", "subject": "New login — London (your workplace)", "sender": "Device: Your office MacBook, Chrome Browser", "isPhish": False}
        ]
    },

    # Q7 - select_all (Password Recipe #1)
    {
        "local_id": 7, "format": "select_all", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Ingredients of a Strong Password",
        "hint": "A strong password is LONG and COMPLEX. Personal details found on social media do NOT count as security!",
        "explain": "Think of a password like a recipe — you need the right ingredients. The four critical ones are: enough length (12+ characters), and variety across all four character types (uppercase, lowercase, numbers, symbols). Personal info is findable online, so it offers zero protection!",
        "reveal": "The correct ingredients are: 12+ characters, 1 uppercase letter, 1 number, and 1 symbol. Your pet's name and street address are WRONG — hackers find these on social media and try them first in personalised attacks. Keep them OUT of your passwords!",
        "correctAnswer": "Correct: 12+ characters, 1 uppercase, 1 number, 1 symbol (@,!,#...)",
        "questionText": "Password Recipe! You are making Strong Password Soup. Select ALL the correct ingredients that make a password truly secure:",
        "options": [
            "At least 12 characters long",
            "At least 1 UPPERCASE letter",
            "At least 1 number (0-9)",
            "At least 1 symbol (!, @, #, $)",
            "Your pet's name",
            "Your street address"
        ],
        "correctFlags": [
            "At least 12 characters long",
            "At least 1 UPPERCASE letter",
            "At least 1 number (0-9)",
            "At least 1 symbol (!, @, #, $)"
        ]
    },

    # Q8 - scavenger_hunt (Sticky Note Detective)
    {
        "local_id": 8, "format": "scavenger_hunt", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Physical Password Security",
        "hint": "Which items in this office have actual passwords written on them in plain sight for anyone walking by to see?",
        "explain": "Writing passwords on sticky notes, under keyboards, or on whiteboards is a 'physical security failure'. Any visitor, cleaner, or thief can see them. NEVER write a real password anywhere visible. Use a password manager app instead!",
        "reveal": "The 3 security risks: the sticky note with WiFi password, the sticky note with email password, and the keyboard with a bank PIN taped underneath. The monitor showing a company sales report is fine — documents are visible but contain no login credentials.",
        "correctAnswer": "Click: WiFi sticky note, Email password note, Bank PIN under keyboard",
        "questionText": "Sticky Note Detective! You're in a messy office. Find and click ALL items that are security risks — passwords written where anyone can see them!",
        "objects": [
            {"id": "o1", "icon": "📝", "label": "Sticky Note: WiFi password = admin123", "isRedFlag": True, "top": "15%", "left": "8%"},
            {"id": "o2", "icon": "🖥", "label": "Screen shows: Q3 Sales Report", "isRedFlag": False, "top": "15%", "left": "55%"},
            {"id": "o3", "icon": "📝", "label": "Note stuck on screen: Email pass = Summer22", "isRedFlag": True, "top": "60%", "left": "8%"},
            {"id": "o4", "icon": "⌨", "label": "Taped under keyboard: Bank PIN 4821", "isRedFlag": True, "top": "60%", "left": "55%"}
        ]
    },

    # Q9 - branching_narratives (One-Key Jigsaw)
    {
        "local_id": 9, "format": "branching_narratives", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Password Reuse Danger",
        "hint": "Imagine one master key that opens your home, your car AND your bank vault. If someone steals it...",
        "explain": "Password reuse is one of the most dangerous habits in cybersecurity. When a website is hacked, attackers automatically try the same email and password on hundreds of other sites — banks, email, shopping. This automated attack is called 'Credential Stuffing'.",
        "reveal": "Correct! When you reuse passwords, one breach unlocks everything. A hacker uses automated tools to try your stolen credentials on every major website within hours. The fix is a unique password for every account — a Password Manager makes this easy!",
        "questionText": "One-Key Jigsaw! You use the same password 'Sunshine22' for your Email, Bank, AND Netflix. Your email gets hacked. What happens next?",
        "options": [
            "Nothing — different websites protect each other and keep your other accounts safe",
            "Only the email account is at risk, banks have extra security that blocks it",
            "All three accounts are now at risk — hackers will try the same password on every website!"
        ],
        "correctAnswer": "All three accounts are now at risk — hackers will try the same password on every website!"
    },

    # Q10 - decision_simulator (Breach Reaction #1)
    {
        "local_id": 10, "format": "decision_simulator", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Responding to a Data Breach",
        "hint": "In a real fire you do not wait to see if your house burns — you act immediately. Same rule applies to hacked accounts!",
        "explain": "When a website you use is breached, your credentials may already be in hackers' hands. The faster you change your password, the shorter the window for an attacker to use it. Waiting even a few days can lead to full account takeover with devastating consequences.",
        "reveal": "Right move! Immediately logging in and changing your password to a new strong unique one is the crucial first step. Then check if you used that same password on other sites and change those too. Delete browser history does absolutely nothing to help!",
        "questionText": "Breaking News Alert! Your Social Media Site Was Hacked — Passwords Stolen! You have an account there. What do you do IMMEDIATELY?",
        "options": [
            "Wait and see if your account actually gets taken over before doing anything",
            "Immediately log in and change your password to a new strong unique one",
            "Just delete your browser history and clear cookies on your device"
        ],
        "correctAnswer": "Immediately log in and change your password to a new strong unique one"
    },

    # Q11 - capture_the_flag (Shoulder Surfer Spotter)
    {
        "local_id": 11, "format": "capture_the_flag", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Shoulder Surfing Awareness",
        "hint": "One person in this coffee shop is clearly more interested in someone ELSE's screen than in their own activity!",
        "explain": "Shoulder surfing is when someone watches over your shoulder while you type your password, PIN, or private messages. It is a low-tech but very effective attack in public spaces — cafes, trains, libraries, airports. Always shield your screen when entering sensitive information!",
        "reveal": "Spotted! The person staring at their neighbour's laptop screen is the shoulder surfer. They can memorise your password just by watching. Fix: use a privacy screen filter, angle your laptop away from others, or wait until you are somewhere private to log in.",
        "correctAnswer": "Click: Person staring at neighbour's laptop screen — the shoulder surfer!",
        "questionText": "Shoulder Surfer Spotter! You are in a coffee shop. Someone nearby is watching over a stranger's shoulder as they type their password. Click the SNOOPER!",
        "objects": [
            {"id": "o1", "icon": "☕", "label": "Person ordering coffee at the counter", "isFlag": False, "top": "20%", "left": "8%"},
            {"id": "o2", "icon": "👀", "label": "Person staring at neighbour's laptop screen", "isFlag": True, "top": "20%", "left": "55%"},
            {"id": "o3", "icon": "📱", "label": "Person scrolling on their own phone", "isFlag": False, "top": "62%", "left": "8%"},
            {"id": "o4", "icon": "📚", "label": "Person quietly reading a book", "isFlag": False, "top": "62%", "left": "55%"}
        ]
    },

    # Q12 - password_triage (Drag & Drop Strength Bin #2)
    {
        "local_id": 12, "format": "password_triage", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Spotting Weak Patterns",
        "hint": "P@ssword1 looks tricky but hackers know every letter substitution trick. They test @ for a and 0 for o automatically!",
        "explain": "Many people think replacing letters with symbols (a to @, o to 0) makes passwords uncrackable. But password cracking tools are programmed to try ALL these common substitutions automatically. A truly strong password avoids recognisable words entirely!",
        "reveal": "Results: qwerty123 = WEAK (top keyboard row + sequential numbers, cracked in milliseconds). P@ssword1 = WEAK (common word with predictable substitutions hackers always try). Sunset!Hamster&Cloud7 = STRONG (long, random, unrelated words + symbols + number).",
        "correctAnswer": "WEAK: qwerty123, WEAK: P@ssword1, STRONG: Sunset!Hamster&Cloud7",
        "questionText": "Strength Bin Round 2! These passwords look different but are some still weak? Sort each one correctly — STRONG or WEAK:",
        "passwords": [
            {"id": "pw1", "text": "qwerty123", "isStrong": False},
            {"id": "pw2", "text": "Sunset!Hamster&Cloud7", "isStrong": True},
            {"id": "pw3", "text": "P@ssword1", "isStrong": False}
        ]
    },

    # Q13 - scenario_mcq (Pattern No-Go MCQ)
    {
        "local_id": 13, "format": "scenario_mcq", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Keyboard Pattern Passwords",
        "hint": "Look at a QWERTY keyboard layout. Which password follows a visible physical path across the keys from left to right?",
        "explain": "Keyboard pattern passwords like 'qwerty', '123456', 'asdfghjkl', or 'zxcvbn' are the very first things hacking tools test. Because they follow physical keyboard layouts, there are very few possible patterns and they appear on every hacker's top 1000 list!",
        "reveal": "qwerty123456 is the worst choice — it runs along the top keyboard row then adds sequential numbers. This appears on every leaked password list and gets cracked in under a millisecond. M0unt@in#Sky8 and HorsePurpleRain!7 are far stronger because they use no keyboard patterns.",
        "questionText": "Pattern No-Go! Which of these passwords would a hacking tool crack the FASTEST because it follows a simple keyboard pattern?",
        "options": [
            "qwerty123456 (runs along the top keyboard row then adds numbers 1 to 6)",
            "M0unt@in#Sky8 (random mix with letter substitutions and symbols)",
            "HorsePurpleRain!7 (random unrelated words combined with symbol and number)"
        ],
        "correctAnswer": "qwerty123456 (runs along the top keyboard row then adds numbers 1 to 6)"
    },

    # Q14 - click_flags (Guess the Weakness #2)
    {
        "local_id": 14, "format": "click_flags", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Dictionary Words and Year Attacks",
        "hint": "A season name is a real English word found in every dictionary. A current year is 100% predictable and always tested by hackers!",
        "explain": "Hackers use dictionary attacks that include common words like season names — summer, winter, spring, autumn — and current years. 'Summer2024!' is one of the most common passwords every year. Security researchers track it and hackers know to try it first on any account!",
        "reveal": "Summer is a common dictionary word found in every password cracking dictionary. 2024 is the current year — hackers always append recent years to words automatically. Only the ! symbol was helping — but one symbol cannot save a password built on two easily guessable components!",
        "correctAnswer": "Click: Summer (dictionary word) and 2024 (current year = predictable!)",
        "questionText": "Guess the Weakness Round 2! The password is: Summer2024! — Click on ALL the parts that make it weak and easily crackable by hacking tools:",
        "emailParts": [
            {"id": "p1", "text": "Summer", "isFlag": True},
            {"id": "p2", "text": "2024", "isFlag": True},
            {"id": "p3", "text": "!", "isFlag": False}
        ],
        "correctFlags": ["p1", "p2"]
    },

    # Q15 - cyber_snakes_ladders (Cracker Tug-of-War #2)
    {
        "local_id": 15, "format": "cyber_snakes_ladders", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Brute Force Attack Defence",
        "hint": "A brute force attack tries EVERY possible combination. What single factor makes that take billions of years instead of minutes?",
        "explain": "Brute force attacks work by trying every possible combination of characters. A 6-character password has about 19 billion possible combinations — crackable in minutes. A 16-character password has more combinations than atoms in the observable universe — mathematically impossible to crack in a human lifetime!",
        "reveal": "Length is your number one defence against brute force! A 16+ character password makes brute force computationally impossible even with the fastest supercomputers. Changing your password every week does not help — a hacker can crack a short password in minutes regardless of how often you rotate it!",
        "questionText": "Cracker Tug-of-War Round 2! A hacker bot is running a Brute Force Attack — it will try EVERY possible character combination until it breaks in. Choose your best defence:",
        "scenario": "HACKER BOT: Brute Force in progress — testing: a, b, c, ..., Aa1!, Aa2! (billions of guesses per second!)",
        "options": [
            "Use a short but complex-looking password like Ab#1! (only 5 characters long)",
            "Use a VERY LONG password of 16 or more characters (e.g. BlueTigerEating!99Pizza) — length makes brute force mathematically impossible",
            "Change your password every single week to stay ahead of the hacker bot"
        ],
        "correctAnswer": "Use a VERY LONG password of 16 or more characters (e.g. BlueTigerEating!99Pizza) — length makes brute force mathematically impossible"
    },

    # Q16 - password_builder (Symbol Scramble)
    {
        "local_id": 16, "format": "password_builder", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Upgrading a Weak Password",
        "hint": "You need all four types: UPPERCASE + lowercase + number + symbol. Hit 8 or more characters. Avoid the year 2024 — it counts as personal info!",
        "explain": "Upgrading a weak base word by adding symbols and numbers is better than nothing, but the key is ensuring all four character types are present and the total length is sufficient. The combination of variety plus length is what makes a password genuinely resistant to attacks.",
        "reveal": "A combination like Pass + word + ! + ABC + 99 gives you Password!ABC99 — 14 characters, uppercase (P and ABC), lowercase (assword), number (99), symbol (!), no personal info. That is a strong password! Avoid 2024 as it is a predictable year hackers always test!",
        "correctAnswer": "Use: uppercase + lowercase + number + symbol pieces, avoid 2024 (personal year info)",
        "questionText": "Symbol Scramble! Take these password pieces and drag them together to make the STRONGEST possible password. Watch the strength meter and aim for the top!",
        "pieces": [
            {"id": "p1", "text": "Pass", "type": "word", "isPersonalInfo": False},
            {"id": "p2", "text": "word", "type": "word", "isPersonalInfo": False},
            {"id": "p3", "text": "!", "type": "symbol", "isPersonalInfo": False},
            {"id": "p4", "text": "@X", "type": "symbol", "isPersonalInfo": False},
            {"id": "p5", "text": "ABC", "type": "word", "isPersonalInfo": False},
            {"id": "p6", "text": "99", "type": "number", "isPersonalInfo": False},
            {"id": "p7", "text": "2024", "type": "number", "isPersonalInfo": True},
            {"id": "p8", "text": "#", "type": "symbol", "isPersonalInfo": False}
        ]
    },

    # Q17 - adaptive_inbox (MFA Gatekeeper #2)
    {
        "local_id": 17, "format": "adaptive_inbox", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Identifying Suspicious Login Attempts",
        "hint": "Watch for: wrong city, unusual time (middle of the night), unknown device, or too many failed attempts. All are major red flags!",
        "explain": "Modern accounts send login notifications when someone signs in from a new device or location. This is your early warning system. Denying suspicious logins immediately can stop a hacker from accessing your account even if they already have your password!",
        "reveal": "Good gating! The login from Russia at 2:30 AM on an unknown Android phone — DENY. The one showing 50 failed password attempts first from China — definitely DENY (that is a hacker caught in the act!). Your home MacBook in London — APPROVE, that is clearly you!",
        "correctAnswer": "APPROVE: home MacBook London. DENY: Russia 2:30AM unknown phone, China 50 failed attempts",
        "questionText": "MFA Gatekeeper Round 2! More login notifications arriving. Tap SAFE to APPROVE the real ones and PHISH to DENY the suspicious ones:",
        "emails": [
            {"id": "r1", "subject": "Login from Russia at 2:30 AM", "sender": "Unknown Android phone — first time ever seen", "isPhish": True},
            {"id": "r2", "subject": "Login from London UK — your home", "sender": "Your MacBook Air — Chrome Browser", "isPhish": False},
            {"id": "r3", "subject": "Login from China after 50 failed password attempts!", "sender": "Unknown Windows PC — suspicious activity", "isPhish": True}
        ]
    },

    # Q18 - select_all (Password Recipe #2 — BAD ingredients)
    {
        "local_id": 18, "format": "select_all", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "What Weakens a Password",
        "hint": "Think: what information do attackers already know about you from social media? That is exactly what they try first!",
        "explain": "Personal information weakens passwords because it is often publicly available. Hackers use personalised dictionary attacks that include your name, pet's name, birthday, and hometown. Using things only a randomly generated computer could produce — like a mix of symbols and unrelated words — is far safer.",
        "reveal": "The spoiled ingredients: your birthday year (predictable), your pet's name (found on social media), a dictionary word by itself (in every cracking database), and your street name (public record). A random symbol like @ by itself is actually a GOOD ingredient — it adds real complexity!",
        "correctAnswer": "Spoiled (weak) ingredients: birthday year, pet's name, alone dictionary word, street name",
        "questionText": "Password Recipe Round 2! You are cleaning up a weak password soup. Select ALL the SPOILED ingredients that make a password easy to hack:",
        "options": [
            "Your birthday year (e.g. 1998 or 2001)",
            "Your pet's name (e.g. Max, Bella, or Biscuit)",
            "A random symbol like @ or ! by itself",
            "A common dictionary word on its own (e.g. sunshine or dragon)",
            "Your street name or house number"
        ],
        "correctFlags": [
            "Your birthday year (e.g. 1998 or 2001)",
            "Your pet's name (e.g. Max, Bella, or Biscuit)",
            "A common dictionary word on its own (e.g. sunshine or dragon)",
            "Your street name or house number"
        ]
    },

    # Q19 - scavenger_hunt (Logout Speedrun)
    {
        "local_id": 19, "format": "scavenger_hunt", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Logging Out on Shared Devices",
        "hint": "Which browser tabs and apps show an ACTIVE logged-in session on this public library computer?",
        "explain": "Staying logged into accounts on shared or public computers such as libraries, cafes, or hotels is extremely dangerous. Anyone who uses the computer next can access your emails, view your bank balance, or post as you. ALWAYS click Logout before leaving any shared device!",
        "reveal": "You found all three! Gmail logged in, Online Banking active, and LinkedIn still signed in are all serious risks on a public library computer. The App Store showing Not Logged In is perfectly safe. Always look for and click Logout or Sign Out before you walk away!",
        "correctAnswer": "Click logout: Gmail (logged in), Online Banking (active session), LinkedIn (still signed in)",
        "questionText": "Logout Speedrun! You are in a public library. Someone left without logging out. Find ALL the dangerous open sessions and click them before a stranger sits down!",
        "objects": [
            {"id": "o1", "icon": "📧", "label": "Gmail — Logged In on public library PC!", "isRedFlag": True, "top": "15%", "left": "8%"},
            {"id": "o2", "icon": "🏦", "label": "Online Banking — Active open session!", "isRedFlag": True, "top": "15%", "left": "55%"},
            {"id": "o3", "icon": "📱", "label": "App Store — Not Logged In", "isRedFlag": False, "top": "62%", "left": "8%"},
            {"id": "o4", "icon": "💼", "label": "LinkedIn — Still Signed In on shared PC!", "isRedFlag": True, "top": "62%", "left": "55%"}
        ]
    },

    # Q20 - branching_narratives (Account Recovery Trivia)
    {
        "local_id": 20, "format": "branching_narratives", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Security Question Safety",
        "hint": "Real banks have official secure processes. They would NEVER cold-call you and ask you to blurt out your security answer over the phone!",
        "explain": "Security questions are only safe if your answers cannot be guessed from your social media or public records. Better still, treat security question answers like passwords — use completely random fake answers and store them in your password manager so only you know them!",
        "reveal": "Hanging up and calling the bank on their official number is always the right move. Real banks NEVER proactively call you to ask for security answers — that is a classic social engineering attack designed to steal your account recovery information to take over your account!",
        "questionText": "Account Recovery Trivia! A caller says they are from your bank: 'Can you confirm your security question answer — your pet's name?' What should you do?",
        "options": [
            "Tell them your pet's name — they said they are from the bank so it must be safe",
            "Hang up immediately and call the bank back using the official number on their real website",
            "Give them a fake pet name to confuse them and then continue the call"
        ],
        "correctAnswer": "Hang up immediately and call the bank back using the official number on their real website"
    },

    # Q21 - the_imposter (Security Question Risk Spotter)
    {
        "local_id": 21, "format": "the_imposter", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Safe Security Question Answers",
        "hint": "Which colleague is sharing information that could help a hacker reset THEIR account by answering their security question?",
        "explain": "Security question answers are only as strong as their secrecy. Using your real mother's maiden name, real pet name, or real school name means anyone who knows you — or checks your social media — may be able to reset your password and lock you out of your own account entirely!",
        "reveal": "Tom is the risk! His mum's maiden name 'Smith' might be findable on Facebook, genealogy sites, or public records. Priya and Lena are being smart — they use completely random fake answers that no one could find through research. Treat security answers like passwords: always random!",
        "questionText": "Security Question Spotter! Three colleagues are chatting about their account security in the office. Which one is accidentally sharing DANGEROUS information?",
        "messages": [
            {"sender": "Priya", "text": "I use totally random fake answers for security questions — like BluePurpleFish22 instead of my real pet name. No one can guess it!", "isPhish": False},
            {"sender": "Tom", "text": "My security question is my mum's maiden name. It's Smith — pretty common anyway so I figured it's fine to use!", "isPhish": True},
            {"sender": "Lena", "text": "I treat security question answers like extra passwords — completely random strings I save in my password manager app.", "isPhish": False}
        ],
        "options": ["Priya", "Tom", "Lena"],
        "correctAnswer": "Tom"
    },

    # Q22 - decision_simulator (Breach Reaction #2)
    {
        "local_id": 22, "format": "decision_simulator", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Post-Breach Action Plan",
        "hint": "Your password may already be in a hacker's hands. If you used the same password elsewhere, what does that mean for those accounts?",
        "explain": "When your email is in a data breach, hackers run automated 'credential stuffing' attacks — trying your stolen email and password on hundreds of other websites within hours. Changing your email password is step one, but checking for password reuse across other accounts is equally critical!",
        "reveal": "Changing your email password immediately is essential AND then auditing for password reuse is the complete correct response. Simply logging out does nothing — the hacker already has your password, not your session. Waiting is the absolute worst option as losses can multiply rapidly!",
        "questionText": "Security Alert! HaveIBeenPwned.com shows your email address appeared in a data breach 3 months ago. Your account still works. What is the MOST important action?",
        "options": [
            "Just log out of your email on all devices — that should solve the problem",
            "Change your email password immediately to a new strong unique one AND check if you used that password on any other sites too",
            "Wait a few more months and see if anything bad actually happens before taking action"
        ],
        "correctAnswer": "Change your email password immediately to a new strong unique one AND check if you used that password on any other sites too"
    },

    # Q23 - spot_weak (Pattern No-Go #2)
    {
        "local_id": 23, "format": "spot_weak", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Identifying Sequential Password Patterns",
        "hint": "Look carefully at each password. Which one follows a completely predictable sequence that any hacker would recognise instantly?",
        "explain": "Sequential and predictable patterns are password killers. 'abcd1234' runs through the alphabet and numbers in perfect order. 'password123' is literally the word 'password'. These top the 'most common passwords' lists and are tested automatically in the first second of any hacking attempt!",
        "reveal": "abcd1234 is the weakest by far — sequential alphabet followed by sequential numbers is one of the most common passwords globally. Security databases have it flagged and it falls in milliseconds. Gr33nRabb!t#99 and Ocean#TigerMoon88 are much stronger because they use no predictable sequences!",
        "questionText": "Pattern No-Go Round 2! Which of these three passwords is the WEAKEST and would be cracked the fastest by any hacking tool?",
        "options": [
            "abcd1234 (alphabet then numbers in perfect sequence — extremely predictable!)",
            "Gr33nRabb!t#99 (letter substitutions with a symbol and number mixed in)",
            "Ocean#TigerMoon88 (random unrelated words with symbols and numbers)"
        ],
        "correctAnswer": "abcd1234 (alphabet then numbers in perfect sequence — extremely predictable!)"
    },

    # Q24 - spot_the_difference (Strong vs Weak Password Comparison)
    {
        "local_id": 24, "format": "spot_the_difference", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Comparing Password Strength",
        "hint": "Count the characters in each. Look at the variety — which one uses MORE types? Length AND variety together is what matters most!",
        "explain": "Two passwords can look visually similar but differ hugely in strength. The two key factors are: length (more characters means exponentially longer to crack) and variety (using all 4 types: uppercase, lowercase, numbers, and symbols). A password with all 4 types AND 12 or more characters is extremely strong.",
        "reveal": "mountain123 is WEAK: only 11 characters, all lowercase letters, no symbols. M0unt@in#Sky8!TrEe is STRONG: 18 characters, uses uppercase, letter substitutions, multiple symbols, and numbers. The difference is length AND character variety — the more of both you have, the more secure the password is!",
        "questionText": "Spot the Stronger Password! Two passwords are shown side by side. Compare them carefully — what is the KEY difference that makes one MUCH stronger than the other?",
        "brandName": "Password Strength Comparison",
        "urlReal": "M0unt@in#Sky8!TrEe  (STRONG — 18 chars)",
        "urlFake": "mountain123  (WEAK — 11 chars)",
        "options": [
            "The length and variety of character types used (uppercase, symbols, numbers all together)",
            "The number of vowels contained in the password string",
            "The position of the capital letter within the password"
        ],
        "correctAnswer": "The length and variety of character types used (uppercase, symbols, numbers all together)"
    },

    # Q25 - sequence_builder (Steps to Create a Strong Password)
    {
        "local_id": 25, "format": "sequence_builder", "difficulty": "beginner",
        "gameName": "password", "game_key": "password", "level_name": "beginner",
        "concept": "Password Creation Best Practices",
        "hint": "Think logically: you cannot SAVE a password before you have CREATED it. You cannot turn on 2FA until the password exists. What is the natural step-by-step order?",
        "explain": "Creating a strong password is a process, not a single action. Following the correct steps ensures you end up with a strong password, a secure storage solution, and a backup protection layer. Skipping the strength check or forgetting to enable 2FA are the two most common mistakes people make!",
        "reveal": "Correct order: 1 — Think of 4 random words, 2 — Join them with symbols and numbers, 3 — Check strength meter shows Strong or Excellent, 4 — Save securely in password manager, 5 — Enable 2FA for an extra security layer. This complete process gives you maximum protection!",
        "questionText": "Password Creation Sequence! Drag and arrange these 5 steps in the CORRECT ORDER for creating a truly secure account password from scratch:",
        "steps": [
            {"id": "s1", "text": "Think of 4 random unrelated words (e.g. Blue, Tiger, Lamp, Rocket)", "correctOrder": 0},
            {"id": "s2", "text": "Join them together with symbols and numbers (e.g. BlueTiger!Lamp99Rocket)", "correctOrder": 1},
            {"id": "s3", "text": "Check the password strength meter — aim for Strong or Excellent rating", "correctOrder": 2},
            {"id": "s4", "text": "Save it securely in a trusted password manager app", "correctOrder": 3},
            {"id": "s5", "text": "Enable 2-Factor Authentication (2FA) on the account for an extra layer of security", "correctOrder": 4}
        ]
    }
]

result = col.insert_many(questions)
count = col.count_documents({'game_key': 'password', 'level_name': 'beginner'})
print("Inserted: " + str(len(result.inserted_ids)) + " questions")
print("Total password beginner questions in DB: " + str(count))
print("")
print("Question order verification (no consecutive same formats):")
for i, q in enumerate(questions):
    prev = questions[i-1]['format'] if i > 0 else "NONE"
    flag = " <<< CONSECUTIVE!" if i > 0 and q['format'] == prev else ""
    print("  Q" + str(q['local_id']).rjust(2) + ": " + q['format'] + flag)

client.close()
