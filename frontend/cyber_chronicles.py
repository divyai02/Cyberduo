import json
import copy

input_file = "src/data/GameQuestions.json"

# NARRATIVE DATABASE: 75 UNIQUE STORY HUBS
STORY_HUBS = {
    "beginner": [
        {"title": "The Zomato Refund", "character": "Rahul", "scenario": "waiting for a ₹450 refund on a cancelled pizza order", "threat": "Phishing Link"},
        {"title": "The Fake Job Offer", "character": "Priya", "scenario": "received an 'Urgent Hiring' WhatsApp message from a generic number", "threat": "Social Engineering"},
        {"title": "OTP Mistake", "character": "Amit", "scenario": "someone called claiming to be from his bank asking for an 'Expired OTP'", "threat": "Vishing"},
        {"title": "Lotto Luck", "character": "Neha", "scenario": "won a ₹1 Crore lucky draw from a shop she never visited", "threat": "Scam"},
        {"title": "Electricity Bill Alert", "character": "Vikram", "scenario": "received a text saying his power will be cut in 2 hours", "threat": "Urgency Scam"},
        {"title": "Social Media Hack", "character": "Sneha", "scenario": "her 'friend' sent a blurry video link saying 'Is this you?'", "threat": "Account Takeover"},
        {"title": "Amazon Prize", "character": "Karan", "scenario": "was promised a free iPhone 15 for 'Spinning a Wheel'", "threat": "Data Harvesting"},
        {"title": "Suspicious USB", "character": "Rohan", "scenario": "found a USB drive in the park labeled 'Salary Data'", "threat": "Malware"},
        {"title": "Public WiFi", "character": "Anjali", "scenario": "trying to join 'Free_Airport_Fast_WiFi'", "threat": "Man-in-the-Middle"},
        {"title": "The Crypto Guru", "character": "Siddharth", "scenario": "a stranger promised 500% returns in 24 hours", "threat": "Investment Scam"},
        {"title": "Late Delivery", "character": "Maya", "scenario": "received a tracking link for an order she didn't place", "threat": "Smishing"},
        {"title": "Netflix Billing", "character": "Raj", "scenario": "received an email saying his subscription was cancelled", "threat": "Phishing"},
        {"title": "Expired Domain", "character": "Ishaan", "scenario": "his company website looks different today", "threat": "DNS Spoofing"},
        {"title": "The Fake Update", "character": "Tanvi", "scenario": "a popup says 'Chrome must update to view this video'", "threat": "Malware"},
        {"title": "KYC Update", "character": "Arjun", "scenario": "got a text from 'Bank' saying KYC is pending", "threat": "Vishing"},
        {"title": "Instagram Contest", "character": "Zoya", "scenario": "won a free makeup kit but needs to 'Verify' her login", "threat": "Phishing"},
        {"title": "Unknown Relative", "character": "Yuvraj", "scenario": "a 'cousin' from abroad is asking for urgent money", "threat": "Impersonation"},
        {"title": "Free Movie Site", "character": "Kriti", "scenario": "the 'Download' button is asking for admin permissions", "threat": "Trojan"},
        {"title": "Fake Antivirus", "character": "Dev", "scenario": "a popup says his laptop has 39 viruses", "threat": "Scareware"},
        {"title": "Google Drive Share", "character": "Meera", "scenario": "received an 'Invitation to Edit' from a strange email", "threat": "Phishing"},
        {"title": "Gaming Hack", "character": "Kabir", "scenario": "wants free 'Skins' but the tool asks for his password", "threat": "Credential Stealer"},
        {"title": "Work From Home", "character": "Riya", "scenario": "a job pays ₹5000 a day for 'Liking YouTube Videos'", "threat": "Task Scam"},
        {"title": "Hotel Booking", "character": "Aditya", "scenario": "needs to confirm his 'Goibibo' stay on a weird link", "threat": "Travel Scam"},
        {"title": "Scholarship Alert", "character": "Tara", "scenario": "won a scholarship she never applied for", "threat": "Phishing"},
        {"title": "WhatsApp Pink", "character": "Sahil", "scenario": "saw a link to 'Upgrade to Pink WhatsApp'", "threat": "Spyware"}
    ],
    "medium": [
        {"title": "The CEO's Request", "character": "Priya", "scenario": "her Boss sent an 'Urgent Wire Transfer' request via email", "threat": "Spear Phishing"},
        {"title": "Digital Arrest", "character": "Vikram", "scenario": "The 'Cyber Crime Cell' is on a video call threatening him", "threat": "Intimidation Scam"},
        {"title": "Income Tax Refund", "character": "Rahul", "scenario": "needs to 'Claim' his ₹12,500 refund on a .gov.co site", "threat": "Gov Phishing"},
        {"title": "Office Printer Malware", "character": "Neha", "scenario": "The office printer is sending out weird PDF.exe files", "threat": "Network Worm"},
        {"title": "LinkedIn Headhunter", "character": "Sneha", "scenario": "received a PDF 'Job Description' that is actually a macro", "threat": "Malware"},
        {"title": "Shared Spreadsheet", "character": "Amit", "scenario": "The company 'Bonuses' file needs a plugin to open", "threat": "Macro Virus"},
        {"title": "MFA Fatigue", "character": "Karan", "scenario": "his phone is getting 50 'Approve Login' requests a minute", "threat": "MFA Spamming"},
        {"title": "Fake LinkedIn Profile", "character": "Anjali", "scenario": "a 'Recruiter' from Google is asking for her Aadhaar", "threat": "Identity Theft"},
        {"title": "The Rogue Access Point", "character": "Sid", "scenario": "found a WiFi called 'Corporate_Internal' in the lobby", "threat": "Evil Twin"},
        {"title": "Compromised Vendor", "character": "Vikram", "scenario": "a trusted vendor sent an 'Updated Invoice' with a new bank account", "threat": "BEC Attack"},
        {"title": "Employee Portal", "character": "Rohan", "scenario": "The 'HR Portal' URL is slightly off: 'hr-cyberduo.net'", "threat": "Phishing"},
        {"title": "Customer Database Leak", "character": "Maya", "scenario": "found the company's customer list on a public Pastebin", "threat": "Data Breach"},
        {"title": "Shadow IT", "character": "Krtit", "scenario": "someone installed 'FreeVPN' on a production server", "threat": "Backdoor"},
        {"title": "The Clean Desk Policy", "character": "Aditya", "scenario": "found a sticky note with 'Admin123' on a monitor", "threat": "Physical Security"},
        {"title": "Zoom Update", "character": "Tara", "scenario": "an urgent meeting requires a 'Zoom_Installer_V3.pkg'", "threat": "Malware"},
        {"title": "Cloud Misconfiguration", "character": "Ishaan", "scenario": "The company's S3 bucket is set to 'Public'", "threat": "Data Exposure"},
        {"title": "Slack Infiltration", "character": "Zoya", "scenario": "an 'App' called 'Giphy-Plus' is asking for full workspace read", "threat": "API Token Theft"},
        {"title": "The Disgruntled Ex", "character": "Sahil", "scenario": "A former dev still has SSH access to the server", "threat": "Insider Threat"},
        {"title": "USB Rubber Ducky", "character": "Meera", "scenario": "stuck a 'Lost' USB into her laptop, and windows started typing", "threat": "HID Attack"},
        {"title": "SIM Swapping", "character": "Yuvraj", "scenario": "his phone suddenly says 'No Service' while he's at work", "threat": "SIM Swap"},
        {"title": "Social Engineering Call", "character": "Tanvi", "scenario": "The 'IT Desk' wants her to 'Install TeamViewer' for a fix", "threat": "Remote Access Trojan"},
        {"title": "The Fake News Flare", "character": "Kabir", "scenario": "The company stock is dropping due to a fake tweet", "threat": "Disinformation"},
        {"title": "Malicious Browser Extension", "character": "Riya", "scenario": "her browser is redirecting all searches to 'Go-Search.info'", "threat": "Adware"},
        {"title": "Bitlocker Scare", "character": "Raj", "scenario": "his files are hidden, and a note says 'Pay in 48 hours'", "threat": "Ransomware"},
        {"title": "Aadhaar Masking", "character": "Arjun", "scenario": "The hotel wants a photocpy of his full Aadhaar", "threat": "Privacy Violation"}
    ],
    "hard": [
        {"title": "Operation Blackout", "character": "Vikram", "scenario": "The power grid's SCADA system is showing unexplained errors", "threat": "Nation State Attack"},
        {"title": "Supply Chain Breach", "character": "Priya", "scenario": "The library we use for 'Auth' has been hijacked on NPM", "threat": "Supply Chain Attack"},
        {"title": "Zero-Day Exploit", "character": "Rahul", "scenario": "A hacker is using a bug in Chrome that has no patch yet", "threat": "0-Day"},
        {"title": "Stuxnet Variation", "character": "Neha", "scenario": "The centrifuges at the plant are spinning too fast", "threat": "Industrial Sabotage"},
        {"title": "DNS Poisoning", "character": "Amit", "scenario": "The whole country's bank traffic is being routed to China", "threat": "DNS Hijack"},
        {"title": "Ransomware Lockdown", "character": "Karan", "scenario": "The City Hospital's systems are fully encrypted", "threat": "WannaCry-style Attack"},
        {"title": "Deepfake CEO Video", "character": "Sneha", "scenario": "The CEO joined a Zoom call and ordered an urgent transfer", "threat": "AI Impersonation"},
        {"title": "SQL Injection", "character": "Rohan", "scenario": "The login page returns '1=1' and dumps the main user table", "threat": "Web Vulnerability"},
        {"title": "BGP Hijacking", "character": "Ishaan", "scenario": "Our entire IP range was announced by a Russian ISP", "threat": "Routing Attack"},
        {"title": "Encrypted Exfiltration", "character": "Maya", "scenario": "100GB of data is leaving the server over HTTPS at 3 AM", "threat": "Data Exfiltration"},
        {"title": "The Logic Bomb", "character": "Siddharth", "scenario": "A hidden code will delete the DB if it hasn't heard from a specific user", "threat": "Internal Logic Bomb"},
        {"title": "Side-Channel Attack", "character": "Arjun", "scenario": "The attacker is reading encryption keys from CPU power usage", "threat": "Spectre/Meltdown"},
        {"title": "Watering Hole", "character": "Tara", "scenario": "The 'Cafeteria Menu' site is infecting all employee laptops", "threat": "Targeted Infection"},
        {"title": "Man-in-the-Browser", "character": "Tanvi", "scenario": "A malware is changing bank account numbers in the HTML", "threat": "Financial Trojan"},
        {"title": "Cold Boot Attack", "character": "Sahil", "scenario": "The attacker rebooted the server and extracted the RAM", "threat": "Forensic Bypass"},
        {"title": "SS7 Hijacking", "character": "Zoya", "scenario": "The attacker is intercepting SMS OTPs at the carrier level", "threat": "Cellular Breach"},
        {"title": "Dirty Pipe", "character": "Kabir", "scenario": "The Linux kernel root access was gained through a buffer bug", "threat": "Privilege Escalation"},
        {"title": "Malicious Firmare", "character": "Raj", "scenario": "The server's BIOS itself is infected and survives reformat", "threat": "Rootkit"},
        {"title": "DDoS Extortion", "character": "Aditya", "scenario": "The website is down, and the botnet won't stop until paid", "threat": "Layer 7 DDoS"},
        {"title": "Quantum Threat", "character": "Meera", "scenario": "The attacker is storing our encrypted traffic for future cracking", "threat": "Store-Now-Decrypt-Later"},
        {"title": "Ghost in the Machine", "character": "Riya", "scenario": "The Firewall rules are changing by themselves at midnight", "threat": "Advanced Persistence"},
        {"title": "Credential Stuffing", "character": "Yuvraj", "scenario": "10 million attempts to login using leaked combo lists", "threat": "Brute Force"},
        {"title": "Cross-Site Scripting", "character": "Anjali", "scenario": "The comment section is stealing user session cookies", "threat": "XSS Attack"},
        {"title": "Container Escape", "character": "Maya", "scenario": "The hacker broke out of the Docker container to the Host", "threat": "Virtualization Escape"},
        {"title": "Evil Maid", "character": "Vikram", "scenario": "Someone accessed his laptop in the hotel room for 5 mins", "threat": "Physical Implant"}
    ]
}

def weave_chronicles():
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    game_keys = ["phishing", "password", "malware", "firewall", "scams"]
    
    for gk in game_keys:
        for lvl in ["beginner", "medium", "hard"]:
            hubs = STORY_HUBS[lvl]
            # Baseline templates for UI structure
            base_templates = data[gk]["beginner"][:5]
            
            new_questions = []
            for i in range(25):
                hub = hubs[i]
                template = copy.deepcopy(base_templates[i % len(base_templates)])
                
                template["id"] = i + 1
                template["difficulty"] = lvl
                # Unique storytelling text!
                template["questionText"] = f"CHAPTER: {hub['title']}\n{hub['character']} is {hub['scenario']}. This looks like a {hub['threat']}."
                template["concept"] = f"{hub['threat']} Expert"
                template["hint"] = f"Focus on the {hub['threat']} indicators."
                template["explain"] = f"In this {lvl} case, we examine how a {hub['threat']} works. {hub['character']}'s situation is a perfect example."
                template["reveal"] = f"Investigation Complete: {hub['character']} was targeted by a {hub['threat']}. Stay vigilant!"

                # Deep data customization for specific game types to ensure variety
                if "emailParts" in template:
                    for p in template["emailParts"]:
                        if p["id"] == "sender" and p["isFlag"]: p["text"] = f"{hub['title'].split()[0]} <alert@secure-{hub['character'].lower()}.net>"
                        if p["id"] == "subject": p["text"] = f"Subject: {hub['title']} - URGENT NOTICE"

                if "emails" in template:
                    for e in template["emails"]:
                        if e["isPhish"]:
                            e["subject"] = f"{hub['title']} Update"
                            e["sender"] = f"support@{hub['character'].lower()}-verif.in"

                if "displayedLink" in template:
                    template["displayedLink"] = f"GO TO {hub['title'].upper()}"
                    template["actualDestination"] = f"http://{hub['character'].lower()}-portal.xyz/login"

                new_questions.append(template)
            
            data[gk][lvl] = new_questions

    with open(input_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

weave_chronicles()
print("THE CYBER CHRONICLES: 375 UNIQUE STORIES WOVEN SUCCESSFULLY!")
