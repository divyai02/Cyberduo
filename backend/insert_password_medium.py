# gitleaks:allow
# NOTE: This file contains EXAMPLE passwords and simulated threats for educational purposes.
# They are NOT real credentials and are safe to be in the repository.

from dotenv import load_dotenv
import os
load_dotenv()
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGO_URI'))
col = client['cyberduo']['questions']

col.delete_many({'game_key': 'password', 'level_name': 'medium'})

questions = [

    # Q1 — the_imposter (Password Vault Audit: find the duplicate password)
    {
        "local_id": 1, "format": "the_imposter", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Password Manager Audit — Finding Duplicate Reused Passwords",
        "hint": "A duplicate password is when the SAME password is used for more than one account. Check the password shown in each vault entry — which account shares EXACTLY the same password as NatWest_Banking? That account is the dangerous weak link!",
        "explain": "Password reuse is the single biggest account security risk. When one site is breached, attackers test the stolen password on all major banks, email providers, and shopping platforms — a technique called 'credential stuffing'. If your Instagram password matches your banking password, an Instagram breach immediately threatens your bank account. Every account needs a unique, strong password.",
        "reveal": "Instagram_Social is the dangerous duplicate! Its password 'SunnyBeach2023!' is IDENTICAL to the NatWest Banking password. If Instagram is breached (social media sites are frequently breached), 'SunnyBeach2023!' would be immediately tested on UK banking sites by automated bots. Rotating Instagram to a unique password eliminates this single point of failure. A password manager generates unique passwords for every account automatically!",
        "questionText": "Vault Audit! Your password manager shows 4 accounts. The security audit found a DUPLICATE — the same password is used for your banking account AND one other account. Which account is the DANGEROUS DUPLICATE that must be rotated?",
        "messages": [
            {"sender": "NatWest_Banking", "text": "🏦 Password: SunnyBeach2023! | Last changed: 8 months ago | Status: HIGH RISK account", "isPhish": False},
            {"sender": "Google_Email", "text": "📧 Password: Kx9$mR2!vLpQ | Last changed: 2 months ago | Status: UNIQUE — safe", "isPhish": False},
            {"sender": "Instagram_Social", "text": "📸 Password: SunnyBeach2023! | Last changed: 8 months ago | ⚠️ SAME PASSWORD AS BANK!", "isPhish": True},
            {"sender": "Amazon_Shopping", "text": "🛒 Password: wP8#nT2$yR6! | Last changed: 1 month ago | Status: UNIQUE — safe", "isPhish": False}
        ],
        "options": ["NatWest_Banking", "Google_Email", "Instagram_Social", "Amazon_Shopping"],
        "correctAnswer": "Instagram_Social"
    },

    # Q2 — decision_simulator (MFA Timing Attack: unsolicited 2FA code)
    {
        "local_id": 2, "format": "decision_simulator", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "MFA Timing Attack — Responding to an Unsolicited 2FA Code",
        "hint": "A legitimate 2FA code ONLY arrives when YOU just initiated a login. If a 6-digit code appears on your phone and you did NOT just try to log in anywhere — someone else has your password and is actively attempting to log into your account RIGHT NOW!",
        "explain": "MFA Timing Attacks happen when an attacker has already obtained your username and password (from a breach or phishing). They log in, triggering your MFA code to be sent to your phone. They then call or message you pretending to be the bank or IT team asking for the code 'for verification'. Never share MFA codes with ANYONE — and always block the attempt if you receive an unsolicited code.",
        "reveal": "Click 'I did not request this' to block the login attempt, then change your NatWest password immediately! The unsolicited code confirms someone has your password and is attempting to use it RIGHT NOW. The 5-minute timer means they are waiting for you to either share the code or do nothing. Blocking the attempt stops them; changing your password prevents future attempts using the same stolen credential.",
        "questionText": "MFA Alert! Your phone shows unexpectedly: '🔒 NatWest: Your one-time passcode is 847291. Valid for 5 minutes. NEVER share this code.' You have NOT tried to log into NatWest today. What do you do?",
        "options": [
            "Wait 5 minutes for the code to expire harmlessly — if you do not enter it, nothing bad can happen",
            "Click 'I did not request this' to block the login attempt, then immediately change your NatWest password",
            "Enter the code to see what account it logs you into — this will help identify where the attack is coming from"
        ],
        "correctAnswer": "Click 'I did not request this' to block the login attempt, then immediately change your NatWest password"
    },

    # Q3 — password_builder (Entropy Bar: build a 100% strength password)
    {
        "local_id": 3, "format": "password_builder", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Password Entropy — Building a Maximum Strength Password",
        "hint": "Drag pieces from all 4 categories into the drop zone: UPPERCASE + lowercase + Numbers + Symbols. Keep personal info pieces OUT of your password — pet names and years are guessable from social media! The strength bar charges to 100% only when all 4 types are present with no personal info.",
        "explain": "Password entropy measures unpredictability — the number of unique combinations an attacker must search. Using all 4 character types (A-Z, a-z, 0-9, !@#$) exponentially increases the search space. A 12-character password using all 4 types has trillions of possible combinations. Password managers generate and store this complexity automatically — you only need to remember one master password.",
        "reveal": "A 100% strength password requires: 8+ characters, at least one UPPERCASE letter, at least one lowercase letter, at least one number (0-9), at least one symbol (!@#$%), and NO personal information pieces. Pieces marked with red warning signs (like 'fluffy' and '1990') are personal info — guessable through social media research. Use only the random mixed character pieces for a fully charged strength bar!",
        "questionText": "Entropy Bar Challenge! Drag password components from the toolbox into the drop zone. Hit 100% charge on the strength bar by including ALL 4 character types — and keep personal information OUT!",
        "pieces": [
            {"id": "p1", "text": "Kx9$", "type": "mixed", "isPersonalInfo": False},
            {"id": "p2", "text": "mR2!", "type": "mixed", "isPersonalInfo": False},
            {"id": "p3", "text": "vLp3", "type": "mixed", "isPersonalInfo": False},
            {"id": "p4", "text": "Q#nT", "type": "mixed", "isPersonalInfo": False},
            {"id": "p5", "text": "fluffy", "type": "lower", "isPersonalInfo": True},
            {"id": "p6", "text": "1990", "type": "number", "isPersonalInfo": True},
            {"id": "p7", "text": "BLUE", "type": "upper", "isPersonalInfo": False},
            {"id": "p8", "text": "@#$%", "type": "symbol", "isPersonalInfo": False}
        ]
    },

    # Q4 — select_all (Breach Ripple Effect: select all accounts using same password)
    {
        "local_id": 4, "format": "select_all", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Credential Stuffing — Identifying All Accounts at Risk After a Breach",
        "hint": "Select EVERY account where you reused the SAME password as the breached gaming site. Attackers test stolen credentials on hundreds of services simultaneously within hours of a breach becoming public — every duplicate is at identical risk!",
        "explain": "Credential stuffing is fully automated: within hours of a breach, bots test stolen username/password pairs against all major banking sites, email providers, shopping platforms, and social media simultaneously. If you used 'GameR0ck2023!' on Netflix, Spotify, AND Amazon, all three are compromised the moment the gaming site database is cracked — even without those sites ever being directly attacked.",
        "reveal": "Lock down all four accounts! Netflix, Spotify, Amazon, and Gmail Backup all use 'GameR0ck2023!' — the same password compromised by the gaming breach. Your Work Microsoft account and Bank account use different unique passwords (they are safe). Change affected accounts immediately, prioritising email first (email access enables password resets for ALL other accounts). A dedicated password manager eliminates this risk by generating unique passwords automatically.",
        "correctAnswer": "Select all 4 reused-password accounts: Netflix, Spotify, Amazon, Gmail Backup",
        "questionText": "Breach Alert! 🚨 'GameZone Pro hacked — millions of passwords exposed!' You used the same password 'GameR0ck2023!' on GameZone AND on other sites. Select ALL accounts that need IMMEDIATE password rotation:",
        "options": [
            "Netflix — you used 'GameR0ck2023!' here too",
            "Work Microsoft Account — IT mandated a different password for this one",
            "Spotify — you used 'GameR0ck2023!' here too",
            "Amazon — you used 'GameR0ck2023!' here too",
            "Gmail Backup Account — you used 'GameR0ck2023!' here too",
            "Bank Account — you always use a completely unique password for banking"
        ],
        "correctFlags": [
            "Netflix — you used 'GameR0ck2023!' here too",
            "Spotify — you used 'GameR0ck2023!' here too",
            "Amazon — you used 'GameR0ck2023!' here too",
            "Gmail Backup Account — you used 'GameR0ck2023!' here too"
        ]
    },

    # Q5 — scenario_mcq (Passphrase Complexity: best armored passphrase)
    {
        "local_id": 5, "format": "scenario_mcq", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Passphrase Armoring — Building a Strong, Memorable Password",
        "hint": "The strongest passphrase uses 4 RANDOM, UNRELATED words connected by symbols and numbers. The words should NOT form a recognisable phrase, should not relate to each other, and should not contain personal information!",
        "explain": "Armored passphrases are simultaneously more memorable AND stronger than random character strings. Key requirements: random unrelated words (not a famous phrase or lyric), symbols between EVERY word (not just at the end), at least one number embedded, and capitalisation variation. 'Gr@pe!Wr3nch*D@rk#P1an' uses 4 random words and would take thousands of years to crack with current GPU technology.",
        "reveal": "'Gr@pe!Wr3nch*D@rk#P1an' is the strongest! It uses 4 completely unrelated words with symbol armor and numbers between every word. 'password123!' is a top-10 most-guessed password worldwide. 'MyDog_Fluffy_Forever!' uses personal information (pet name) and weak connectors. 'Summer2024!' is short, seasonal, and easily guessable — summer years are commonly tested in wordlist attacks.",
        "questionText": "Passphrase Challenge! The Security Guard only grants access to passphrases that pass ALL rules: 4+ unrelated words, symbols between each word, includes a number, NO personal info. Which passphrase PASSES the guard?",
        "options": [
            "password123! — short, common, top-10 most guessed password globally",
            "MyDog_Fluffy_Forever! — personal info (pet name), weak underscore connectors only",
            "Gr@pe!Wr3nch*D@rk#P1an — 4 unrelated words, symbols AND numbers between each word, all 4 character types",
            "Summer2024! — seasonal word + year + symbol — frequently tested in wordlist attacks"
        ],
        "correctAnswer": "Gr@pe!Wr3nch*D@rk#P1an — 4 unrelated words, symbols AND numbers between each word, all 4 character types"
    },

    # Q6 — scavenger_hunt (Hardware Keylogger Detection at public computer)
    {
        "local_id": 6, "format": "scavenger_hunt", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Hardware Keylogger Detection — Physical Security at Shared Computers",
        "hint": "A hardware keylogger is a small physical device inserted between a keyboard cable and the computer's USB or PS/2 port. It records EVERY keystroke — including all passwords — to internal memory that the attacker retrieves later. Look for any unexpected device in the cable connections!",
        "explain": "Hardware keyloggers are physically small (the size of a USB drive) and require no software installation — making them completely invisible to antivirus and security scans. They capture keystroke data in hardware memory. Attackers plant them on public computers, hotel PCs, library workstations, and shared office hotdesks. Always physically inspect keyboard connections before typing passwords on any shared computer.",
        "reveal": "The keylogger is the small grey cylindrical device plugged between the keyboard cable and the computer's USB port! It looks like a harmless adapter but records every keystroke. Rule for public computers: physically check the keyboard cable where it connects to the computer. If there is ANY device between the keyboard and the computer that you cannot explain, do not type passwords — use your own device instead.",
        "correctAnswer": "Click the small grey device inserted between the keyboard cable and the computer USB port",
        "questionText": "Keylogger Guard! You are at an airport lounge public computer and need to check your email. BEFORE typing anything — find and click the HARDWARE KEYLOGGER hidden in this computer setup!",
        "objects": [
            {"id": "o1", "icon": "🖥️", "label": "PC Tower — the main computer unit (safe, normal component)", "isRedFlag": False, "top": "10%", "left": "40%"},
            {"id": "o2", "icon": "⌨️", "label": "Keyboard — standard QWERTY keyboard (safe, normal device)", "isRedFlag": False, "top": "72%", "left": "10%"},
            {"id": "o3", "icon": "🔌", "label": "Small grey barrel device between keyboard cable and USB port — THIS IS THE KEYLOGGER!", "isRedFlag": True, "top": "60%", "left": "38%"},
            {"id": "o4", "icon": "🖱️", "label": "Mouse — standard optical mouse (safe, normal device)", "isRedFlag": False, "top": "72%", "left": "65%"}
        ]
    },

    # Q7 — click_flags (Forgotten Account Cleanup: click old dormant apps to delete)
    {
        "local_id": 7, "format": "click_flags", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Digital Footprint Reduction — Deleting Old Dormant Accounts",
        "hint": "Click every old app or service you no longer actively use. Dormant accounts from 2017-2020 often still store your old password, real name, address, and payment details — with potentially weaker security than modern services hosting the same data!",
        "explain": "Old unused accounts are a hidden security risk that grows over time. They often store: the password you used years ago (before good password hygiene), your real contact details and payment history, and social connections. When those old services are breached (increasingly common), attackers try your old credentials on every modern service you use now. Deleting dormant accounts removes these exposure points permanently.",
        "reveal": "Delete all four old dormant accounts: Photo-editor-online.com (2018), FreeGameSite.net (2019), OldForumPro.com (2017), and Giveaway-site.io (2020). Active accounts you use regularly (Gmail, WhatsApp) should be retained but regularly audited. Schedule an account audit every 6-12 months — search your email for 'Welcome to' or 'Account created' messages to discover forgotten registrations.",
        "correctAnswer": "Click 4 dormant old accounts for deletion: photo-editor, FreeGameSite, OldForumPro, Giveaway-site",
        "questionText": "Account Map Cleanup! This map shows your registered online accounts. Click all the OLD DORMANT accounts you should DELETE to reduce your digital attack surface:",
        "emailParts": [
            {"id": "p1", "text": "📧 Gmail (2015) — active daily email, in regular use — KEEP", "isFlag": False},
            {"id": "p2", "text": "🎨 Photo-editor-online.com (2018) — registered once, never returned — DELETE", "isFlag": True},
            {"id": "p3", "text": "🎮 FreeGameSite.net (2019) — played 3 times, completely forgotten — DELETE", "isFlag": True},
            {"id": "p4", "text": "💬 WhatsApp (2017) — messaging app used every single day — KEEP", "isFlag": False},
            {"id": "p5", "text": "💬 OldForumPro.com (2017) — joined for one question, never visited again — DELETE", "isFlag": True},
            {"id": "p6", "text": "🎁 Giveaway-site.io (2020) — entered one competition, site looks abandoned — DELETE", "isFlag": True}
        ],
        "correctFlags": ["p2", "p3", "p5", "p6"]
    },

    # Q8 — spot_fake (Security Question Sabotage: safest approach)
    {
        "local_id": 8, "format": "spot_fake", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Security Question Sabotage — Using Fictional Unfindable Answers",
        "hint": "Real answers to security questions are almost always findable through social media, public records, or social engineering. The ONLY safe approach is a completely fictional, memorable answer that no researcher could find because it does not exist in the real world!",
        "explain": "Security questions are fundamentally insecure because their 'correct' answers are findable data: your mother's maiden name is in genealogy records and old Facebook posts; your first pet's name is tagged in Instagram photos; your hometown is on your LinkedIn and Facebook profiles. The sabotage technique: use memorable fictional answers stored in your password manager alongside the account credentials.",
        "reveal": "'TurboJet777' stored in your password manager is the safe approach! It is unfindable because it is completely invented — no social media, genealogy record, or social engineering can reveal a fictional random answer. Real maiden names, pet names, and birthdays are all discoverable through digital research. Use a fictional answer and store it alongside the account in your password manager so you can always retrieve it for account recovery.",
        "questionText": "Security Question Setup! You are creating an account and must answer 'What is your mother's maiden name?' Which approach gives you the STRONGEST security?",
        "options": [
            "Enter your mother's actual real maiden name — security questions exist to verify real identity so truthful answers are required",
            "Leave the field blank or type '???' — skipping security questions removes this security layer entirely",
            "Enter a fictional memorable answer like 'TurboJet777' and store it in your password manager alongside this account"
        ],
        "correctAnswer": "Enter a fictional memorable answer like 'TurboJet777' and store it in your password manager alongside this account"
    },

    # Q9 — sequence_builder (Vault Migration: Chrome to dedicated manager)
    {
        "local_id": 9, "format": "sequence_builder", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Password Manager Migration — Browser to Dedicated Vault (Safe Order)",
        "hint": "Export FIRST, import SECOND, VERIFY the import succeeded THIRD, THEN delete the export file, THEN clear the browser. Never wipe the browser before confirming the dedicated manager has everything — you risk losing access to accounts!",
        "explain": "Migrating from a browser's built-in password manager to a dedicated vault (Bitwarden, 1Password, Dashlane) requires strict sequence discipline. The export file is an unencrypted plain-text list of ALL your passwords — it must be securely deleted immediately after the import is confirmed. Clearing the browser before verifying the import succeeded would leave you locked out of all accounts. The verification step is critical and commonly skipped.",
        "reveal": "Correct migration sequence: 1) Export passwords from Chrome as CSV (create the backup), 2) Import the CSV into Bitwarden, 3) VERIFY the import by checking 5-10 key accounts are present and correct in Bitwarden (critical step!), 4) Securely delete the plain-text CSV export file (it contains all your passwords unencrypted — urgent to delete!), 5) Remove saved passwords from Chrome to prevent dual exposure. This sequence guarantees zero password loss and minimises the window of plain-text exposure.",
        "questionText": "Vault Migration! You are moving all passwords from Chrome's built-in manager to Bitwarden. Arrange these 5 migration steps in the CORRECT order to ensure no passwords are lost and no security gaps appear:",
        "steps": [
            {"id": "s1", "text": "Export all saved passwords from Chrome's built-in manager as a .CSV file", "correctOrder": 0},
            {"id": "s2", "text": "Import the .CSV file into Bitwarden and complete the import process", "correctOrder": 1},
            {"id": "s3", "text": "Verify the import by checking 5-10 important accounts are correctly saved in Bitwarden", "correctOrder": 2},
            {"id": "s4", "text": "Securely delete the plain-text .CSV export file — it contains ALL your passwords unencrypted!", "correctOrder": 3},
            {"id": "s5", "text": "Remove all saved passwords from Chrome's built-in manager to prevent duplicate exposure", "correctOrder": 4}
        ]
    },

    # Q10 — branching_narratives (Session Timeout: stranger sits next to you at bank computer)
    {
        "local_id": 10, "format": "branching_narratives", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Session Security — Manual Logout on Shared or Observed Computers",
        "hint": "On any shared or public computer, ALWAYS manually log out of every sensitive account before leaving or when observed. Do NOT rely on auto-timeout — sessions can remain open for 30+ minutes. A banking session left open is a banking session anyone can use!",
        "explain": "Browser session cookies on shared computers remain active after you close windows — for minutes to hours depending on the site's timeout settings. Anyone who sits down after you can hit Ctrl+Shift+T to restore closed tabs and immediately access your active sessions. Manual logout deletes the session token on the server, making session restoration impossible. Always log out explicitly from banking, email, and sensitive accounts on any non-personal device.",
        "reveal": "Manual Logout immediately, then transact on your own phone! A banking session left open on a shared computer is a catastrophic security exposure. The library auto-timeout might take 30 minutes. The stranger next to you could access your account in 10 seconds using the 'restore closed tabs' browser shortcut after you leave. Your personal phone's banking app is far safer for sensitive transactions you cannot complete before leaving a shared PC.",
        "questionText": "Session Race! You are logged into your bank account on a shared library computer. You still have £200 to transfer — but a stranger just sat down in the adjacent chair and is clearly waiting for your computer. What do you do?",
        "options": [
            "Quickly finish all your transactions — you were here first and the person can wait their turn patiently",
            "Click Manual Logout from your banking session immediately, then complete transactions on your own mobile device",
            "Minimise the browser window so the banking session is hidden from the stranger's view"
        ],
        "correctAnswer": "Click Manual Logout from your banking session immediately, then complete transactions on your own mobile device"
    },

    # Q11 — link_inspector (Fake Password Reset URL: hover to reveal phishing domain)
    {
        "local_id": 11, "format": "link_inspector", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Fake Password Reset Email — Inspecting the Hidden Link URL",
        "hint": "Real password reset links from Google are 100% on accounts.google.com. A reset button that actually links to ANY other domain — even one containing the word 'google' — is a credential-harvesting phishing page!",
        "explain": "Fake password reset emails exploit legitimate urgency about account security. The button text looks reassuring ('Secure Password Reset', 'Recover Your Account') but the actual href points to an attacker-controlled domain. Hovering over any link before clicking reveals the real destination in the browser's status bar. Real reset links from Google, Microsoft, Apple are always on their verified domains — never third-party registration domains.",
        "reveal": "PHISHING! The reset button links to 'accounts-google-security-verify.com' — not accounts.google.com. Real Google password resets originate from accounts.google.com only. A domain containing the word 'google' but with additional words appended is a registered phishing domain. Clicking this link takes you to a fake login page that harvests your CURRENT password under the guise of 'verifying your identity to reset'.",
        "questionText": "Fake Reset Alert! An email says 'Your Google password reset was requested. Click below to reset your account securely.' Hover over the reset button to see the actual link destination. Safe or Phishing?",
        "displayedLink": "[ 🔐 SECURE GOOGLE PASSWORD RESET ] → [Hover to reveal the real destination URL]",
        "actualDestination": "https://accounts-google-security-verify.com/reset?token=g1k9mx&track=user",
        "correctAnswer": "Phishing"
    },

    # Q12 — click_flags (Dictionary Filter: remove common dictionary words from proposed password)
    {
        "local_id": 12, "format": "click_flags", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Dictionary Attack Defence — Removing Guessable Words from Passwords",
        "hint": "Dictionary attacks test millions of common words, names, and phrases against password databases. Click and remove EVERY common recognisable word or year — any dictionary word in a password makes it dramatically weaker. Leave only random character strings!",
        "explain": "Dictionary attacks precompute hashes for millions of real words, common substitutions (password→p@ssw0rd), and popular phrases — and match them against stolen password hashes in seconds. A password containing ANY dictionary word, even with number substitutions, is susceptible. 'sunshine', 'dragon', 'hello', and year numbers like '2024' all appear in standard cracking wordlists used by tools like Hashcat and John the Ripper.",
        "reveal": "Remove: 'sunshine' (top-25 most common passwords globally), 'dragon' (in every cracking wordlist), 'hello' (universal dictionary word), and '2024' (current year — always in modern wordlists). Keep: 'kX9$', 'mP7#', and '@wQ6' — these random character strings are not in any dictionary. A password containing only random character strings cannot be cracked by dictionary attacks, only by brute force (which is computationally unfeasible for properly mixed characters).",
        "correctAnswer": "Remove 4 dictionary/common words: sunshine, dragon, hello, 2024",
        "questionText": "Dictionary Filter! This proposed password mixes random strings with dangerously common words. Click and REMOVE all the dictionary words and common terms — leave only the random character strings!",
        "emailParts": [
            {"id": "p1", "text": "kX9$ — Random mixed characters (KEEP — not in any cracking dictionary)", "isFlag": False},
            {"id": "p2", "text": "sunshine — Top-25 most used password globally (REMOVE — in every wordlist!)", "isFlag": True},
            {"id": "p3", "text": "mP7# — Random mixed characters (KEEP — not in any cracking dictionary)", "isFlag": False},
            {"id": "p4", "text": "dragon — Extremely common word, in every standard cracking wordlist (REMOVE!)", "isFlag": True},
            {"id": "p5", "text": "hello — Universal common word, top-10 password worldwide (REMOVE!)", "isFlag": True},
            {"id": "p6", "text": "@wQ6 — Random characters with symbol and number (KEEP — genuinely unpredictable)", "isFlag": False},
            {"id": "p7", "text": "2024 — Current year — always tested in modern password crackers (REMOVE!)", "isFlag": True}
        ],
        "correctFlags": ["p2", "p4", "p5", "p7"]
    },

    # Q13 — the_imposter #2 (Fake Breach Notification: phishing disguised as security alert)
    {
        "local_id": 13, "format": "the_imposter", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Fake Breach Notification — Phishing Disguised as a Legitimate Security Alert",
        "hint": "Legitimate breach notification services send from their verified domain — HaveIBeenPwned sends from @haveibeenpwned.com only. Any alert asking you to 'click to confirm the breach' or 'verify your identity' through an email link is phishing — real alerts just inform, they never request authentication!",
        "explain": "Fake breach notifications piggyback on real breach news. When a major breach is announced, attackers immediately send fake 'breach notification' emails impersonating the breached company or HaveIBeenPwned. The phishing emails contain credential-harvesting links disguised as 'secure reset portals'. Real breach notifications from legitimate services inform you of the breach details — they never require you to authenticate via an email link to 'confirm' your exposure.",
        "reveal": "The phishing email is from 'security@haveibeenpwned.alert.net'! The real HIBP notification service sends ONLY from @haveibeenpwned.com — never from a '.alert.net' subdomain. The instruction to 'click here to confirm your account was in the breach and reset your password via our secure portal' is the credential harvest mechanism. Real HIBP emails simply tell you which breach your email appeared in — no link clicking or authentication required to view the information.",
        "questionText": "Breach Alert Inbox! Three notifications arrived. One is a phishing attack disguised as a legitimate breach security alert. Which sender is the IMPOSTER?",
        "messages": [
            {"sender": "security@linkedin.com", "text": "Your account appeared in a data breach. Your password has been reset as a security precaution. Visit linkedin.com directly to set a new password.", "isPhish": False},
            {"sender": "noreply@haveibeenpwned.com", "text": "Your email was found in the 'GameZone Pro' data breach. No action needed here — visit the breached site directly to change your password there.", "isPhish": False},
            {"sender": "security@haveibeenpwned.alert.net", "text": "URGENT: Your account was found in a breach! Click here to confirm your account was affected and reset your password via our secure portal immediately.", "isPhish": True}
        ],
        "options": ["security@linkedin.com", "noreply@haveibeenpwned.com", "security@haveibeenpwned.alert.net"],
        "correctAnswer": "security@haveibeenpwned.alert.net"
    },

    # Q14 — spot_fake (Pass-Hash Visualizer: which statement correctly describes hashing)
    {
        "local_id": 14, "format": "spot_fake", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Password Hashing — One-Way Cryptographic Storage",
        "hint": "Password hashing is ONE-WAY: the same password always produces the same hash, changing ONE character completely changes the entire hash, and you CANNOT reverse a hash back to the original password. Which statement correctly describes ALL of these properties?",
        "explain": "Cryptographic hash functions (bcrypt, Argon2, SHA-256) convert any input into a fixed-length output. Key properties: deterministic (same input = same hash every time), avalanche effect (change one character = completely different hash), and irreversibility (cannot compute the original password from the hash). This means password databases can be stored without exposing actual passwords — even if stolen, attackers must crack the hashes by testing guesses rather than reading passwords directly.",
        "reveal": "Option B correctly describes password hashing! The same password always produces the same hash (deterministic) — but changing even one character produces a completely different hash (avalanche effect) — and you cannot reverse a hash to get the original password (one-way/irreversible). Option A is wrong (hashing is not reversible encryption). Option C is wrong (plain-text passwords are never stored by responsible services). Option D is wrong (a 'collision' where two different passwords produce the same hash is prevented by modern algorithms).",
        "questionText": "Pass-Hash Visualizer! Watch the password turn into a hash code. Which statement CORRECTLY describes how password hashing actually works?",
        "options": [
            "Option A: Your password is encrypted — the service can decrypt and read your original password whenever needed for account verification",
            "Option B: The same password always produces the same hash — changing even ONE character produces a completely different hash that cannot be reversed",
            "Option C: Your actual plain-text password is stored but scrambled with salt characters to make it difficult for hackers to read",
            "Option D: Two different passwords can produce the same hash — so if your password matches someone else's hash, both give identical access"
        ],
        "correctAnswer": "Option B: The same password always produces the same hash — changing even ONE character produces a completely different hash that cannot be reversed"
    },

    # Q15 — scavenger_hunt #2 (Find all accounts using the compromised password in vault)
    {
        "local_id": 15, "format": "scavenger_hunt", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Compromised Password Audit — Finding All Credential-Stuffing Targets",
        "hint": "Find and click EVERY account in the vault mockup that uses the same compromised password 'Blue7Sky!' — each one is an active target for credential-stuffing bots running right now after the breach!",
        "explain": "Credential-stuffing bots run automatically within hours of a breach. They test the compromised credential pair across hundreds of services simultaneously. Every account using 'Blue7Sky!' — not just the breached one — is at equal and immediate risk. Prioritise rotating email accounts first (email access enables password resets for all other accounts), then financial accounts, then social media.",
        "reveal": "The three compromised accounts are Twitter, Dropbox, and Netflix — all using 'Blue7Sky!' (same as the breached service). Gmail, Amazon, and LinkedIn all use different unique passwords (they are safe). Rotate the three compromised accounts immediately, prioritising order: Twitter (most public-facing, most critical to lock down quickly), then Dropbox (may contain sensitive files), then Netflix (lower risk but still exposed). A password manager prevents this entire scenario with unique generated passwords.",
        "correctAnswer": "Click 3 accounts: Twitter, Dropbox, Netflix — all use the breached password 'Blue7Sky!'",
        "questionText": "Compromise Audit! A service was breached and your password 'Blue7Sky!' is compromised. Scan your vault mockup and click EVERY account still using 'Blue7Sky!' — those are all at immediate credential-stuffing risk!",
        "objects": [
            {"id": "o1", "icon": "📧", "label": "Gmail — Password: Kx$9mR2!vL (unique — safe, do not click)", "isRedFlag": False, "top": "5%", "left": "5%"},
            {"id": "o2", "icon": "🐦", "label": "Twitter — Password: Blue7Sky! (SAME — CLICK to flag for immediate rotation!)", "isRedFlag": True, "top": "25%", "left": "5%"},
            {"id": "o3", "icon": "📦", "label": "Dropbox — Password: Blue7Sky! (SAME — CLICK to flag for immediate rotation!)", "isRedFlag": True, "top": "45%", "left": "5%"},
            {"id": "o4", "icon": "🎬", "label": "Netflix — Password: Blue7Sky! (SAME — CLICK to flag for immediate rotation!)", "isRedFlag": True, "top": "65%", "left": "5%"},
            {"id": "o5", "icon": "🛒", "label": "Amazon — Password: wP8#nT2$yR6! (unique — safe, do not click)", "isRedFlag": False, "top": "15%", "left": "55%"},
            {"id": "o6", "icon": "💼", "label": "LinkedIn — Password: mQ3@vB7#kP9$ (unique — safe, do not click)", "isRedFlag": False, "top": "45%", "left": "55%"}
        ]
    },

    # Q16 — select_all (Bad Security Question Choices: all findable-answer questions)
    {
        "local_id": 16, "format": "select_all", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Security Question Risk Assessment — Identifying Guessable Answers",
        "hint": "A security question is risky if its REAL answer can be found through: social media research, public records, genealogy databases, or direct social engineering (just asking). Select ALL questions where a determined attacker could realistically discover your real answer!",
        "explain": "Attackers use Open Source Intelligence (OSINT) to research security question answers before account takeover attempts. Your mother's maiden name is in genealogy records and old Facebook posts. Your first pet's name is in Instagram photo comments. Your hometown is on your LinkedIn profile. Your high school is publicly shared in LinkedIn's Education section. Any question with a discoverable real-world answer should use a fictional stored answer instead.",
        "reveal": "All four real-information questions are dangerous! 'Mother's maiden name' (genealogy databases + Facebook), 'First pet's name' (common social media photo content), 'Childhood hometown' (LinkedIn Education + Facebook location), 'High school' (LinkedIn + reunion group social media). Only the fictional password manager answer is safe — 'TurboJet777' cannot be found through any amount of OSINT because it does not exist in the real world. Store fictional security answers in your password manager.",
        "correctAnswer": "Select all 4 real-info questions — all are findable through social media or public records",
        "questionText": "Security Question Audit! You are setting up a new account's security questions. Select ALL the options that are DANGEROUS because a determined attacker could realistically research the answer:",
        "options": [
            "Mother's maiden name — appears in genealogy records, old Facebook posts, and family social media mentions",
            "First pet's name — extremely common Instagram and Facebook photo content with names tagged by friends",
            "Childhood hometown — visible on LinkedIn profiles, Facebook 'Grew Up In' fields, and hometown reunion groups",
            "Name of high school attended — always visible on LinkedIn's Education section and school reunion pages",
            "Fictional answer in password manager: 'TurboJet777' — completely invented, unfindable through any research"
        ],
        "correctFlags": [
            "Mother's maiden name — appears in genealogy records, old Facebook posts, and family social media mentions",
            "First pet's name — extremely common Instagram and Facebook photo content with names tagged by friends",
            "Childhood hometown — visible on LinkedIn profiles, Facebook 'Grew Up In' fields, and hometown reunion groups",
            "Name of high school attended — always visible on LinkedIn's Education section and school reunion pages"
        ]
    },

    # Q17 — password_builder #2 (Armored Passphrase: build with symbol connectors)
    {
        "local_id": 17, "format": "password_builder", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Armored Passphrase Construction — Assembling Word + Symbol Combinations",
        "hint": "Drag the FOUR random word pieces first, using SYMBOL pieces between each word. Make sure at least one piece contains a NUMBER. Keep the red-highlighted personal info pieces OUT of your passphrase drop zone!",
        "explain": "An armored passphrase is constructed from random unrelated words with symbol and number connectors between each word. 'Gr@pe*Wr3nch#D@rk!Bl@ze' is extremely long, uses all 4 character types, and the words have no logical relationship — making it both memorable and resistant to dictionary and hybrid attacks. The red pieces (personal info) would make the passphrase guessable through social media research — always avoid them.",
        "reveal": "Build by dragging: Gr@pe → * → Wr3nch → # → D@rk → ! → Bl@ze. This creates 'Gr@pe*Wr3nch#D@rk!Bl@ze' — 22 characters with all 4 character types, no personal info, and 4 unrelated words armored with 3 symbol connectors. The strength meter hits 100% because it satisfies all entropy requirements. The personal info piece (fluffy) would reduce the score and introduce guessability — keep it in the toolbox!",
        "questionText": "Armored Passphrase Builder! Assemble the strongest possible passphrase by dragging pieces into the correct order. Use all 4 character types, connect words with symbols, and keep personal information OUT of the password zone!",
        "pieces": [
            {"id": "p1", "text": "Gr@pe", "type": "mixed", "isPersonalInfo": False},
            {"id": "p2", "text": "*", "type": "symbol", "isPersonalInfo": False},
            {"id": "p3", "text": "Wr3nch", "type": "mixed", "isPersonalInfo": False},
            {"id": "p4", "text": "#", "type": "symbol", "isPersonalInfo": False},
            {"id": "p5", "text": "fluffy", "type": "lower", "isPersonalInfo": True},
            {"id": "p6", "text": "D@rk", "type": "mixed", "isPersonalInfo": False},
            {"id": "p7", "text": "!", "type": "symbol", "isPersonalInfo": False},
            {"id": "p8", "text": "Bl@ze", "type": "mixed", "isPersonalInfo": False}
        ]
    },

    # Q18 — spot_the_difference (Real vs Fake Password Manager UI)
    {
        "local_id": 18, "format": "spot_the_difference", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Identifying Fake Password Manager Login Pages",
        "hint": "The real password manager login is always on its own verified domain. Hover the two URLs and read from right-to-left: what is the ROOT domain (the word right before .com or .net)?",
        "explain": "Fake password manager login pages are uniquely dangerous because they harvest your master password — giving attackers access to every password in your vault simultaneously. These phishing pages are meticulously crafted to look pixel-perfect. The URL is the only reliable differentiator: 1Password's real login is always at my.1password.com. Always bookmark your password manager login page and access it only through bookmarks — never through email links or search results.",
        "reveal": "The FAKE is '1password-vault-login.net'! Reading right-to-left: .net TLD → 'login' is part of the domain path → the root domain is '1password-vault' — not '1password.com'. The real 1Password login is exclusively at 'my.1password.com' — a subdomain of 1password.com. Entering your master password on the fake page would give attackers access to every password you have stored. Always bookmark and type password manager URLs directly — never click links to them.",
        "questionText": "Password Manager Trap! Two browser tabs show what looks like your 1Password vault signin page. One is REAL, one is a PHISHING PAGE. Compare the URLs in each card — which is the FAKE?",
        "brandName": "1Password Vault Signin",
        "urlReal": "https://my.1password.com/signin",
        "urlFake": "https://1password-vault-login.net/app/signin",
        "options": [
            "my.1password.com/signin is the real login — it is the official verified 1Password authentication domain",
            "1password-vault-login.net is the PHISHING PAGE — a fake domain harvesting your master password",
            "Both pages look identical — you cannot tell which is real from the URL alone without signing in"
        ],
        "correctAnswer": "1password-vault-login.net is the PHISHING PAGE — a fake domain harvesting your master password"
    },

    # Q19 — sequence_builder #2 (Account Compromise Recovery: correct steps)
    {
        "local_id": 19, "format": "sequence_builder", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Account Compromise Recovery — Correct Step Sequence",
        "hint": "Secure the account FIRST (change password + enable MFA) to cut off the attacker's access, THEN investigate what they accessed, THEN revoke their access permissions, THEN notify affected contacts. Never notify others before securing the account — the attacker might still be inside!",
        "explain": "Account compromise recovery follows a specific critical path: containment first, then assessment, then remediation, then communication. Changing the password (Step 1) cuts off the attacker immediately. Enabling MFA (Step 2) prevents re-entry even if they try again with a new credential. Reviewing activity (Step 3) reveals the full scope. Revoking sessions (Step 4) removes any backdoor access they may have established. Warning contacts (Step 5) is the last step because you need the account secured before announcing the compromise.",
        "reveal": "Correct recovery sequence: 1) Change password immediately (cuts off attacker access), 2) Enable MFA (prevents re-entry), 3) Review login activity (understand the breach scope), 4) Revoke all active sessions and suspicious connected apps, 5) Warn contacts if the attacker sent malicious messages. This sequence prioritises containment before assessment and notification — the most effective incident response order.",
        "questionText": "Instagram Compromised! Your account was hacked and the attacker may have sent messages to your followers. Arrange these 5 recovery steps in the CORRECT sequence:",
        "steps": [
            {"id": "s1", "text": "Change your Instagram password immediately to a new, unique, strong one — cut off the attacker", "correctOrder": 0},
            {"id": "s2", "text": "Enable Two-Factor Authentication (MFA) on your Instagram account — prevent future re-entry", "correctOrder": 1},
            {"id": "s3", "text": "Review Instagram's Recent Login Activity to see when and where the attacker accessed your account", "correctOrder": 2},
            {"id": "s4", "text": "Revoke all active sessions and remove any suspicious apps the attacker may have connected", "correctOrder": 3},
            {"id": "s5", "text": "Message your followers to warn them if the attacker sent malicious links or DMs from your account", "correctOrder": 4}
        ]
    },

    # Q20 — decision_simulator #2 (Public Computer explicit logout)
    {
        "local_id": 20, "format": "decision_simulator", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Public Computer Security — Complete Logout and Session Clearance",
        "hint": "Closing the browser window is NOT the same as logging out! Sessions persist on the server. The next user can restore your closed tabs using Ctrl+Shift+T and instantly access your open banking session — even after you have walked away!",
        "explain": "Browser session cookies on shared computers remain valid on the server even after you close the browser window — for 30 minutes to several hours depending on the site's timeout. The 'restore closed tabs' keyboard shortcut (Ctrl+Shift+T) is common knowledge. Manual logout is the only guaranteed method: it invalidates the session token on the server, making restoration impossible for the next user regardless of what shortcuts they try.",
        "reveal": "Log out explicitly from ALL sensitive accounts AND clear browsing history before closing! Simply closing the browser leaves active session tokens that the next user can restore in 2 seconds. The triple-action procedure: 1) Explicitly log out of each sensitive account (banking, email, social media), 2) Clear browsing data including cookies (Ctrl+Shift+Del in most browsers), 3) Then close the browser. This ensures no residual session or browsing history remains accessible on the shared computer.",
        "questionText": "Library Computer! You have been using a public library PC to access your bank account and email. You are about to leave. What is the CORRECT security procedure before walking away?",
        "options": [
            "Close the browser window and log off the PC — closing the window automatically clears all session cookies and browsing data",
            "Log out explicitly from every sensitive account, clear the browsing history and cookies, then close the browser and log off",
            "Open a new Incognito/Private browsing window for the next user — they will not be able to see any of your session data in a fresh private window"
        ],
        "correctAnswer": "Log out explicitly from every sensitive account, clear the browsing history and cookies, then close the browser and log off"
    },

    # Q21 — traffic_triage (Sort login attempts: legitimate vs suspicious)
    {
        "local_id": 21, "format": "traffic_triage", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Login Activity Monitoring — Classifying Legitimate vs Suspicious Auth Attempts",
        "hint": "ALLOW logins from your usual device (MacBook Air, iPhone 14), your real UK locations, and normal waking hours. BLOCK logins from unfamiliar countries, unusual hours (3AM while you are asleep), or unknown device types you have never used!",
        "explain": "Login monitoring catches account compromise early by identifying behavioural anomalies: geolocation (a foreign country you have never visited), time (login at 3AM when you are normally asleep), device type (Windows PC when you only own Mac and iPhone), and velocity (50 login attempts in 1 minute = automated bot). Enable login notifications on all sensitive accounts so you see suspicious attempts in real-time.",
        "reveal": "ALLOW: London 09:15 MacBook Air (your usual device + normal hour + UK location) and Manchester 19:30 iPhone 14 (your phone + evening hour + UK location visiting family). BLOCK: Moscow 03:47 (foreign country + middle of the night!), and unknown Windows PC 14:22 (you never use Windows — unknown device type!). Both blocked attempts match credential-stuffing or account-takeover attack patterns. Change your password immediately if you see these!",
        "correctAnswer": "ALLOW: London MacBook 09:15, Manchester iPhone 19:30 — BLOCK: Moscow 03:47, Unknown Windows PC",
        "questionText": "Login Monitor! Review these recent Google account login attempts. You use only a MacBook Air and iPhone 14, live in the UK, and sleep 11PM-7AM. Mark each attempt as ALLOW (legitimate) or BLOCK (suspicious):",
        "files": [
            {"id": "f1", "icon": "💻", "name": "Login: London UK — 09:15 — MacBook Air — Chrome (your usual device and location)", "isMalware": False},
            {"id": "f2", "icon": "🌍", "name": "Login attempt: Moscow Russia — 03:47 AM — Unknown device — suspicious browser agent", "isMalware": True},
            {"id": "f3", "icon": "📱", "name": "Login: Manchester UK — 19:30 — iPhone 14 — Safari (your phone, visiting family)", "isMalware": False},
            {"id": "f4", "icon": "🖥️", "name": "Login attempt: 14:22 — Windows PC (unknown OS — you never use Windows!)", "isMalware": True}
        ]
    },

    # Q22 — branching_narratives #2 (HaveIBeenPwned breach response)
    {
        "local_id": 22, "format": "branching_narratives", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "HaveIBeenPwned Alert — Complete Breach Response Procedure",
        "hint": "The MOST COMPLETE response to a HaveIBeenPwned alert changes the compromised site's password AND finds and rotates all reused passwords AND enables MFA everywhere. Doing just one of these three is insufficient — attackers will find the reused versions!",
        "explain": "HaveIBeenPwned monitors breach databases and notifies registered users when their email appears in newly-discovered breach data. When you receive an alert: 1) Note the breach date (your password from that era is compromised), 2) Change the breached service's password immediately, 3) Identify all other accounts using the same password and rotate them too (credential stuffing risk), 4) Enable MFA on all affected accounts especially email (email enables all other password resets). The password audit step is the most commonly missed.",
        "reveal": "The most complete response: Change LinkedIn's password, audit and rotate all reused passwords, then enable MFA on LinkedIn and your email! Simply reading the breach details without acting leaves you exposed. Changing only LinkedIn's password misses all the other accounts using the same password. The MFA step on your primary email is especially critical — email inbox access allows an attacker to reset passwords for every other account that uses that email address.",
        "questionText": "HIBP Alert! 'Your email was found in the LinkedIn data breach from 2023.' What is the MOST COMPLETE correct response?",
        "options": [
            "Visit haveibeenpwned.com to read the full breach details — understanding what happened is the most important first step",
            "Change only your LinkedIn password — the breach was LinkedIn's servers that were compromised so only LinkedIn needs action",
            "Immediately change LinkedIn's password, audit and rotate all other accounts using the same password, then enable MFA on LinkedIn and your email"
        ],
        "correctAnswer": "Immediately change LinkedIn's password, audit and rotate all other accounts using the same password, then enable MFA on LinkedIn and your email"
    },

    # Q23 — file_inspector (Password_Reset_Instructions.exe disguised as .docx)
    {
        "local_id": 23, "format": "file_inspector", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Malicious Executable Disguised as a Password Reset Document",
        "hint": "Hover over the file attachment to see the REAL file type hidden in the metadata. A 'Password Reset Instructions' PDF or Word document is safe to read — but if it is actually an .EXE executable file, it is malware designed to look like a document!",
        "explain": "Attackers disguise malware as expected document types — especially in password and account management contexts where employees expect to receive instructions. Windows hides file extensions by default, so 'PasswordReset_Instructions.exe' saved with a Word icon displays only 'PasswordReset_Instructions' — looking identical to a real .docx file. Hovering over attachments (or enabling 'Show file extensions' in Windows Explorer settings) reveals the true extension before you execute anything.",
        "reveal": "MALWARE! The file is actually 'PasswordReset_Instructions.EXE' — a Windows executable, not a Word document. The Word icon was deliberately set on the executable file by the attacker to make it visually identical to a real document. Running this file would install credential-stealing malware or a keylogger. Permanently fix this: enable 'Show file extensions for known file types' in Windows Explorer settings — this removes the visual deception entirely.",
        "questionText": "File Inspector! An email from 'IT Security Helpdesk' says: 'Please read the attached document for updated password reset procedures.' Hover over the attachment to reveal its real file type. Is it a Safe Document or Malware?",
        "displayedName": "PasswordReset_Instructions.docx [Hover to inspect the real file type metadata]",
        "actualDestination": "⚠️ REAL FILE TYPE: PasswordReset_Instructions.EXE — Windows Executable! This is NOT a Word document — malware disguised with a Word icon!",
        "correctAnswer": "Malware"
    },

    # Q24 — adaptive_inbox (Sort password-related notifications: real vs phishing)
    {
        "local_id": 24, "format": "adaptive_inbox", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Password Notification Email Triage — Real Alerts vs Phishing",
        "hint": "Check sender domain first: real Google sends from @accounts.google.com, real Apple from @email.apple.com, real NatWest from @natwest.com. Any other domain — even a similar-sounding one — is phishing!",
        "explain": "Password-related phishing emails create urgency around account security to make people click quickly without inspecting the sender domain. The 2-second check: does the sender domain EXACTLY match the real company's verified domain? 'outlook-password-reset.com' is NOT microsoft.com. 'natwest-alert.uk' is NOT natwest.com. Legitimate notifications from real services confirm actions YOU took — phishing emails create panic about things you did NOT do.",
        "reveal": "SAFE: Google 'password changed successfully' from accounts.google.com (verified — confirms your own action) and Apple 'new sign-in on iPhone' from email.apple.com (verified Apple subdomain — check your devices if you are unsure). PHISHING: 'Outlook password EXPIRED' from outlook-password-reset.com (NOT microsoft.com!) and 'NatWest Account Locked' from natwest-alert.uk (NOT natwest.com!). The pattern: real services use their own domains; phishing services use lookalike registered domains.",
        "questionText": "Password Notification Triage! Four emails just arrived. Rapidly classify each as SAFE (legitimate) or PHISH (delete!) before the clock runs out:",
        "emails": [
            {"id": "e1", "subject": "Your Google account password was changed successfully", "sender": "no-reply@accounts.google.com", "isPhish": False},
            {"id": "e2", "subject": "URGENT: Your Outlook password has EXPIRED — reset immediately to avoid losing access", "sender": "support@outlook-password-reset.com", "isPhish": True},
            {"id": "e3", "subject": "Apple ID: New sign-in to your account from iPhone in London", "sender": "no_reply@email.apple.com", "isPhish": False},
            {"id": "e4", "subject": "NatWest Alert: Your account has been LOCKED — click here to restore access now", "sender": "security@natwest-alert.uk", "isPhish": True}
        ]
    },

    # Q25 — scenario_mcq (Password Policy Solver)
    {
        "local_id": 25, "format": "scenario_mcq", "difficulty": "medium",
        "gameName": "passwords", "game_key": "password", "level_name": "medium",
        "concept": "Password Policy Compliance — Systematic Rule Evaluation",
        "hint": "Check every policy rule against every password option methodically, one rule at a time. A password only PASSES if it satisfies ALL rules simultaneously — failing even one rule disqualifies it completely!",
        "explain": "Password policy compliance requires systematic one-rule-at-a-time checking: minimum length, required character types, and prohibited patterns (common words, keyboard sequences, names, previous passwords). This methodical approach is used by security auditors, penetration testers, and compliance professionals. Rushing or pattern-matching can miss a single violated rule that disqualifies an otherwise strong-looking password.",
        "reveal": "'Kx9$mR2!vLpQ' is the ONLY compliant password! Rule-by-rule check: ✓ 12 characters exactly, ✓ uppercase (K, L, Q), ✓ lowercase (x, m, v, p), ✓ number (9, 2), ✓ symbol ($, !), ✓ no dictionary words, ✓ no names, ✓ no keyboard sequences. 'StarTrek2024!' fails: 'StarTrek' is a proper noun/cultural reference (qualifies as a name). 'qwerty!Admin9' fails TWO rules: 'qwerty' is a prohibited keyboard sequence AND 'Admin' is a prohibited common word. Always evaluate ALL rules — not just the ones that seem most important!",
        "questionText": "Password Policy Test! Your company's IT policy states: '12+ characters, must include uppercase, lowercase, number AND symbol, with NO dictionary words, no names/cultural references, and no keyboard sequences (like qwerty, 12345, abc).' Which of these THREE passwords is the ONLY fully COMPLIANT one?",
        "options": [
            "StarTrek2024! — 12 chars with all 4 character types (but StarTrek is a proper noun/cultural name — POLICY FAIL!)",
            "qwerty!Admin9 — 13 chars with all 4 types (but qwerty=keyboard sequence AND Admin=common word — DOUBLE POLICY FAIL!)",
            "Kx9$mR2!vLpQ — 12 chars, all 4 types, no dictionary words, no names, no keyboard sequences — POLICY COMPLIANT!"
        ],
        "correctAnswer": "Kx9$mR2!vLpQ — 12 chars, all 4 types, no dictionary words, no names, no keyboard sequences — POLICY COMPLIANT!"
    }

]

result = col.insert_many(questions)
count = col.count_documents({'game_key': 'password', 'level_name': 'medium'})
print("Inserted:", len(result.inserted_ids), "password medium questions")
print("Total password medium in DB:", count)
print("\nFormat order (checking for consecutive duplicates):")
prev = ""
all_ok = True
from collections import Counter
fmt_counts = Counter(q['format'] for q in questions)
for q in questions:
    dup = " <<< CONSECUTIVE DUPLICATE!" if q['format'] == prev else ""
    if dup: all_ok = False
    print(f"  Q{q['local_id']:2}: {q['format']}{dup}")
    prev = q['format']
print("\nFormats used per type:", dict(sorted(fmt_counts.items())))
over = {f: c for f, c in fmt_counts.items() if c > 2}
if over: print("OVER LIMIT:", over)
elif all_ok: print("\nAll good — no consecutive duplicates and all formats <= 2!")
client.close()
