from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv('MONGO_URI'))
col = client['cyberduo']['questions']

# Clear existing hard mal/fire
col.delete_many({'game_key': 'malware', 'level_name': 'hard'})
col.delete_many({'game_key': 'firewall', 'level_name': 'hard'})

mal_hard = [
    {
        "local_id": 1, "format": "file_inspector", "difficulty": "hard",
        "gameName": "malware", "game_key": "malware", "level_name": "hard",
        "concept": "Malware Hex Forensics",
        "hint": "Check the Hex header (Magic Bytes). '4D 5A' (MZ) indicates a Windows Executable (EXE), even if the extension says .pdf!",
        "explain": "Attackers rename malicious .exe files to .pdf or .txt to trick users. In the Hard level, you must inspect the raw Magic Bytes (Hex) to reveal the true file type. MZ (4D 5A) is the signature of a Windows PE file.",
        "displayedName": "Company-Bonus-List.pdf",
        "actualDestination": "HEX HEADER: 4D 5A 90 00 03 00 00 00 (TRUE TYPE: .EXE)",
        "correctAnswer": "Malware",
        "questionText": "File Inspector: You found a PDF on the shared drive. Inspect its raw Hex signature. Is this a safe document or masked malware?"
    },
    {
        "local_id": 2, "format": "file_triage", "difficulty": "hard",
        "gameName": "malware", "game_key": "malware", "level_name": "hard",
        "concept": "Multi-Stage Infection Chains",
        "hint": "Watch for 'Double Extensions' (e.g., .pdf.exe) and files in temporary directories (e.g., %TEMP%).",
        "explain": "Hard-level triage involves identifying stealthy persistence mechanisms. Files in System32 or Temp folders with suspicious names or double extensions are high-priority threats.",
        "files": [
            {"id": "f1", "name": "svchost.exe", "desc": "Location: C:\\Windows\\System32 (Genuine Service)", "icon": "⚙️", "isMalware": False},
            {"id": "f2", "name": "Invoice.pdf.exe", "desc": "Location: %TEMP% folder", "icon": "📄", "isMalware": True},
            {"id": "f3", "name": "update.bin", "desc": "Location: AppData\\Roaming\\Hidden", "icon": "📦", "isMalware": True}
        ],
        "questionText": "File Triage: Your antivirus flagged three suspicious files. Sort them: KEEP the genuine system files and DELETE the malware threats."
    },
    {
        "local_id": 3, "format": "escape_rooms", "difficulty": "hard",
        "gameName": "malware", "game_key": "malware", "level_name": "hard",
        "concept": "Terminal Persistence Removal",
        "hint": "Use 'taskkill /F /IM' followed by the process name to stop a stubborn malicious process.",
        "explain": "Removing malware requires stopping the active process before deleting the file. Hard level simulates a terminal environment where you must use exact commands to neutralize a threat.",
        "terminalOutput": [
            "SCANNING PROCESSES...",
            "PID: 1024 | NAME: explorer.exe (System)",
            "PID: 4096 | NAME: malicious_bot.exe (Threat Detected)",
            "PID: 5120 | NAME: chrome.exe (User)",
            "Action required: Terminate the threat using 'taskkill /F /IM <name>'"
        ],
        "correctAnswer": "taskkill /F /IM malicious_bot.exe",
        "questionText": "Terminal Escape: A Trojan is active. Enter the terminal command to force-kill the malicious process 'malicious_bot.exe'."
    },
    {
        "local_id": 4, "format": "scavenger_hunt", "difficulty": "hard",
        "gameName": "malware", "game_key": "malware", "level_name": "hard",
        "concept": "USB Drop / Rubber Ducky Detection",
        "hint": "Look for unusual hardware plugged into computers, especially in 'unattended' areas like the lobby or breakroom.",
        "explain": "Physical malware delivery (USB Drops) remains a major threat. A 'Rubber Ducky' looks like a USB drive but acts as a keyboard to type malicious commands in seconds.",
        "objects": [
            {"id": "o1", "icon": "🖱️", "label": "Standard USB Mouse", "isRedFlag": False},
            {"id": "o2", "icon": "💾", "label": "Unknown USB Drive in Server Port", "isRedFlag": True},
            {"id": "o3", "icon": "⌨️", "label": "Mechanical Keyboard", "isRedFlag": False},
            {"id": "o4", "icon": "🔌", "label": "Malicious HID 'Rubber Ducky' in Lobby PC", "isRedFlag": True}
        ],
        "questionText": "Hardware Audit: Click on all hardware items that appear suspicious and could be used for physical malware delivery."
    },
    {
        "local_id": 5, "format": "click_flags", "difficulty": "hard",
        "gameName": "malware", "game_key": "malware", "level_name": "hard",
        "concept": "Ransomware Note Analysis",
        "hint": "Check for 'Onion' links, cryptocurrency demands, and threats to leak data (Double Extortion).",
        "explain": "Modern ransomware (Double Extortion) doesn't just encrypt; it steals data and threatens to leak it. Spotting these identifiers helps in incident response and attribution.",
        "emailParts": [
            {"id": "p1", "text": "YOUR FILES ARE ENCRYPTED", "isFlag": False},
            {"id": "p2", "text": "Contact us via: http://v2tor-hidden-service.onion", "isFlag": True},
            {"id": "p3", "text": "Demand: 2.5 BTC (Bitcoin)", "isFlag": True},
            {"id": "p4", "text": "Refuse to pay? We leak 500GB of your private data on our blog.", "isFlag": True}
        ],
        "correctAnswer": "Click: Tor Link, Crypto Demand, Data Leak Threat",
        "questionText": "Ransomware Triage: A ransomware note appeared. Click on the 3 parts that reveal the attacker's 'Double Extortion' strategy."
    }
]

# Fill remaining 20 Mal Hard
for i in range(6, 26):
    mal_hard.append({
        "local_id": i, "format": "file_triage", "difficulty": "hard",
        "gameName": "malware", "game_key": "malware", "level_name": "hard",
        "concept": "Heuristic Threat Hunting",
        "hint": "Look for unsigned binaries or files with random-character names.",
        "explain": "Attackers use 'Randomization' to bypass signature-based detection. Identifying unsigned binaries in critical system paths is a key Hard level skill.",
        "files": [
            {"id": f"f{i}1", "name": "winlogon.exe", "desc": "Microsoft Signed", "icon": "⚙️", "isMalware": False},
            {"id": f"f{i}2", "name": f"ax{i}z7.dll", "desc": "Unsigned Binary in System32", "icon": "📄", "isMalware": True},
            {"id": f"f{i}3", "name": "temp_updater.exe", "desc": "Self-Signed / Untrusted", "icon": "📦", "isMalware": True}
        ],
        "questionText": f"Mission {i}: Threat Hunting. Triage these system components. Identify and BLOCK the suspicious unsigned binaries."
    })

fire_hard = [
    {
        "local_id": 1, "format": "traffic_triage", "difficulty": "hard",
        "gameName": "firewall", "game_key": "firewall", "level_name": "hard",
        "concept": "Egress Filtering / C2 Detection",
        "hint": "Watch for traffic on unusual ports like 4444 (Metasploit) or 6667 (IRC), especially to unknown IPs.",
        "explain": "Egress filtering blocks 'Phone Home' traffic from infected hosts. Hard-level firewalling requires identifying Command & Control (C2) traffic exiting the network on non-standard ports.",
        "files": [
            {"id": "t1", "name": "HTTPS (Port 443)", "desc": "To: google.com (Safe)", "isMalware": False},
            {"id": "t2", "name": "REVERSE SHELL (Port 4444)", "desc": "To: 192.168.99.102 (Internal Malicious)", "isMalware": True},
            {"id": "t3", "name": "DNS (Port 53)", "desc": "To: 8.8.8.8 (Standard)", "isMalware": False}
        ],
        "questionText": "Traffic Triage: Analyze the outgoing network traffic. ALLOW the legitimate requests and BLOCK the malicious Command & Control (C2) traffic."
    },
    {
        "local_id": 2, "format": "kc7_log_hunt", "difficulty": "hard",
        "gameName": "firewall", "game_key": "firewall", "level_name": "hard",
        "concept": "SIEM Log Forensics",
        "hint": "Look for 'Brute Force' patterns: many DENIED attempts followed by one SUCCESS from the same IP.",
        "explain": "Firewall logs reveal brute force attacks. Hard-level logs require spotting 'Low and Slow' attacks that try to bypass threshold-based blocking.",
        "logs": [
            {"id": "l1", "time": "10:00:01", "ip": "1.2.3.4", "event": "LOGIN ATTEMPT", "status": "DENIED"},
            {"id": "l2", "time": "10:00:02", "ip": "1.2.3.4", "event": "LOGIN ATTEMPT", "status": "DENIED"},
            {"id": "l3", "time": "10:00:05", "ip": "1.2.3.4", "event": "LOGIN SUCCESS", "status": "MALICIOUS"}
        ],
        "correctAnswer": "l3",
        "questionText": "Log Hunting: A brute force attack succeeded. Click the log entry that shows the attacker finally gaining unauthorized access."
    },
    {
        "local_id": 3, "format": "adversary_roleplay", "difficulty": "hard",
        "gameName": "firewall", "game_key": "firewall", "level_name": "hard",
        "concept": "Zero-Trust Architecture",
        "hint": "In a Hard level defense, you need a Web Application Firewall (WAF) AND Multi-Factor Authentication (MFA) to reach the Target Value.",
        "explain": "Zero-Trust assumes the network is already breached. You must implement multiple layers (WAF, MFA, Micro-segmentation) to reach the required security 'Target Value' within a limited budget.",
        "budget": 1000,
        "targetValue": 80,
        "assets": [
            {"id": "a1", "name": "Web App Firewall (WAF)", "cost": 400, "value": 45},
            {"id": "a2", "name": "Multi-Factor Auth (MFA)", "cost": 300, "value": 35},
            {"id": "a3", "name": "Standard Antivirus", "cost": 200, "value": 10}
        ],
        "questionText": "Adversary Roleplay: Build a Zero-Trust defense. Select the tools that provide enough 'Threat Value' (80+) to stop an elite hacker, while staying under budget ($1000)."
    },
    {
        "local_id": 4, "format": "escape_rooms", "difficulty": "hard",
        "gameName": "firewall", "game_key": "firewall", "level_name": "hard",
        "concept": "IPTABLES Rule Configuration",
        "hint": "The command 'iptables -A INPUT -p tcp --dport 22 -j DROP' blocks SSH traffic.",
        "explain": "Firewalls are managed via CLI in the real world. Hard level requires knowing the syntax for dropping specific traffic types (like SSH on Port 22) to stop an active intrusion.",
        "terminalOutput": [
            "FIREWALL STATUS: OPEN",
            "ALERT: SSH BRUTE FORCE ON PORT 22",
            "Task: Enter the command to BLOCK all incoming TCP traffic on Port 22.",
            "Usage: iptables -A INPUT -p tcp --dport <port> -j DROP"
        ],
        "correctAnswer": "iptables -A INPUT -p tcp --dport 22 -j DROP",
        "questionText": "Terminal Escape: Your SSH server is under attack! Type the exact command to block Port 22 in the firewall."
    },
    {
        "local_id": 5, "format": "sequence_builder", "difficulty": "hard",
        "gameName": "firewall", "game_key": "firewall", "level_name": "hard",
        "concept": "Incident Response Lifecycle",
        "hint": "Always 'Contain' the threat before you 'Eradicate' it. Recovery comes last.",
        "explain": "Incident Response (IR) follows a strict sequence: Preparation, Identification, Containment, Eradication, Recovery, and Lessons Learned (PICERL).",
        "steps": [
            {"id": "s1", "text": "Identify the Breach Origin", "correctOrder": 0},
            {"id": "s2", "text": "Contain the Threat (Isolate Host)", "correctOrder": 1},
            {"id": "s3", "text": "Eradicate Malware/Rootkits", "correctOrder": 2},
            {"id": "s4", "text": "Recover Systems from Backups", "correctOrder": 3},
            {"id": "s5", "text": "Post-Incident Analysis (Lessons Learned)", "correctOrder": 4}
        ],
        "questionText": "Sequence Builder: Your firewall was bypassed. Arrange the Incident Response steps in the correct order to minimize damage and restore security."
    }
]

# Fill remaining 20 Fire Hard
for i in range(6, 26):
    fire_hard.append({
        "local_id": i, "format": "traffic_triage", "difficulty": "hard",
        "gameName": "firewall", "game_key": "firewall", "level_name": "hard",
        "concept": "DDoS Mitigation",
        "hint": "Identify traffic with 'Spoofed' source IPs or high-frequency SYN packets.",
        "explain": "DDoS attacks saturate network bandwidth. Hard level firewalling involves identifying and dropping SYN flood traffic from forged IP addresses.",
        "files": [
            {"id": f"t{i}1", "name": "SYN Flood", "desc": f"10,000 requests/sec from IP {i}.{i}.{i}.{i}", "isMalware": True},
            {"id": f"t{i}2", "name": "API Request", "desc": "Standard User Login", "isMalware": False},
            {"id": f"t{i}3", "name": "UDP Blast", "desc": "Massive packet burst to random ports", "isMalware": True}
        ],
        "questionText": f"Mission {i}: DDoS Mitigation. Your firewall is overloaded. BLOCK the high-frequency flood traffic and ALLOW legitimate API requests."
    })

col.insert_many(mal_hard)
col.insert_many(fire_hard)

print(f"Inserted 25 Malware Hard and 25 Firewall Hard missions.")
print(f"Total interactive missions: 50")
client.close()
