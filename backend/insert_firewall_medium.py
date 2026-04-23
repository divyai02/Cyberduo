# gitleaks:allow
from dotenv import load_dotenv
import os
load_dotenv('backend/.env')
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGO_URI'))
col = client['cyberduo']['questions']

col.delete_many({'game_key': 'firewall', 'level_name': 'medium'})

questions = [
    # Q1 — kc7_log_hunt (Port 22 SSH Table)
    {
        "local_id": 1, "format": "kc7_log_hunt", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "Log Forensics — SSH Brute Force Detection",
        "hint": "Look for the IP address that has hundreds of 'FAIL' attempts in the same minute. This is a classic botnet brute-force marker.",
        "explain": "Log hunting involves scanning table data for patterns. Legitimate users might fail once or twice, but an attacker will have hundreds of failures (DENIED/FAIL) from the same IP at high speed.",
        "reveal": "Attack Detected! IP 1.2.3.4 is the culprit. It has 500+ DENIED entries in 60 seconds. Blocking this IP immediately stops the brute force attempt on your SSH port.",
        "correctAnswer": "log_2",
        "questionText": "Log Forensic! Your server reports a high CPU load on the SSH service. Scan the connection logs and select the MALICIOUS IP address!",
        "logs": [
            {"id": "log_1", "time": "12:00:01", "ip": "192.168.1.5", "event": "SSH LOGIN", "status": "SUCCESS"},
            {"id": "log_2", "time": "12:00:02", "ip": "1.2.3.4", "event": "SSH AUTH-RETRY", "status": "DENIED"},
            {"id": "log_3", "time": "12:00:02", "ip": "1.2.3.4", "event": "SSH AUTH-RETRY", "status": "DENIED"},
            {"id": "log_4", "time": "12:00:03", "ip": "1.2.3.4", "event": "SSH AUTH-RETRY", "status": "DENIED"}
        ]
    },

    # Q2 — sequence_builder (Firewall Rule Priority)
    {
        "local_id": 2, "format": "sequence_builder", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "Rule Ordering — 'Top Down' Logic",
        "hint": "Firewalls read rules TOP to BOTTOM. Put specific ALLOW rules FIRST, then 'Deny Everything Else' LAST.",
        "explain": "If you place 'Allow Any' at the top, security is disabled. Correct order: 1. Allow needed, 2. Silently Drop/Deny all others (Default Deny).",
        "reveal": "Order: 1) Allow HTTP/S, 2) Allow SSH from My IP, 3) DENY ALL. If 3 was at the top, you'd be locked out!",
        "questionText": "Rule Architect! Arrange these rules to ensure security while allowing web traffic:",
        "steps": [
            {"id": "s1", "text": "ALLOW Inbound TCP Port 80, 443 (Web Traffic)", "correctOrder": 0},
            {"id": "s2", "text": "ALLOW Inbound TCP Port 22 from 'My_IP' (Remote Access)", "correctOrder": 1},
            {"id": "s3", "text": "DENY ALL Inbound Traffic (Security Baseline)", "correctOrder": 2}
        ]
    },

    # Q3 — capture_the_flag (Identifying Data Exfiltration)
    {
        "local_id": 3, "format": "capture_the_flag", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "Outbound Traffic Monitoring (Egress Filtering)",
        "hint": "Look for a large, constant upload from your Database server to an unknown foreign IP address.",
        "explain": "Data exfiltration often hides in HTTPS (Port 443). Anomaly detection catches a server usually sending 1MB but suddenly uploading 50GB.",
        "reveal": "Found it! 'Internal_Database' is sending 25GB to a foreign IP. Classic data theft. BLOCK it!",
        "correctAnswer": "Click the Internal_Database connection sending 25GB to unknown IP",
        "questionText": "Egress Audit! A hacker is UPLOADING your customer data. Find and click the suspicious OUTBOUND connection!",
        "objects": [
            {"id": "o1", "icon": "🖥️", "label": "Reception PC -> Google.com (25MB)", "isFlag": False, "top": "15%", "left": "10%"},
            {"id": "o2", "icon": "🗄️", "label": "Internal_Database -> 194.5.21.88 (25GB UPLOAD!)", "isFlag": True, "top": "40%", "left": "50%"},
            {"id": "o3", "icon": "💻", "label": "Manager Laptop -> Outlook (100MB sync)", "isFlag": False, "top": "70%", "left": "20%"},
            {"id": "o4", "icon": "📺", "label": "Smart TV -> Netflix (1GB)", "isFlag": False, "top": "70%", "left": "70%"}
        ]
    },

    # Q4 — click_flags (Vulnerable Ports)
    {
        "local_id": 4, "format": "click_flags", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "Minimizing Attack Surface",
        "hint": "Ports like 21 (FTP), 23 (Telnet), and 445 (SMB) are dangerous unencrypted legacy ports. Click them!",
        "explain": "Port 21 and 23 send passwords in plain text. 445 (SMB) was the door for WannaCry. Keep them closed to the public internet.",
        "reveal": "Flag Port 21, 23, and 445. Port 443 (HTTPS) is the secure standard and should stay open.",
        "correctAnswer": "Flag 3 ports: 21, 23, and 445",
        "questionText": "Attack Surface Audit! Click ALL the dangerous, unencrypted ports that should be CLOSED immediately!",
        "emailParts": [
            {"id": "p1", "text": "Port 443 — HTTPS (Secure Web Traffic) [KEEP]", "isFlag": False},
            {"id": "p2", "text": "Port 21 — FTP (Plain-text Passwords) [CLOSE]", "isFlag": True},
            {"id": "p3", "text": "Port 23 — Telnet (Plain-text Management) [CLOSE]", "isFlag": True},
            {"id": "p4", "text": "Port 445 — SMB (Ransomware Target) [CLOSE]", "isFlag": True}
        ],
        "correctFlags": ["p2", "p3", "p4"]
    },

    # Q5 — adversary_roleplay (Firewall Budgeting)
    {
        "local_id": 5, "format": "adversary_roleplay", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "Risk-Adjusted Security Budgeting",
        "hint": "You have $10,000 to defend a server worth $100,000. Prioritize 'Stateful Inspection' and 'IPS' over basic 'Logging'.",
        "explain": "Adversary roleplay involves managing resources. A 'Stateful Firewall' provides the highest baseline security, while an 'IPS' stops active exploits. 'Detailed Logging' is good for investigation but doesn't STOP the attack.",
        "reveal": "Mission Success! By choosing the Stateful Firewall ($5k) and IPS ($4k), you blocked the attack with $1k left in budget. Basic logging alone would have let the hacker through while you just 'watched'.",
        "correctAnswer": "High Security Portfolio (Firewall + IPS)",
        "questionText": "Defense Planner! You have a $10,000 budget to defend the HR Server. Choose the portfolio that STOPS the incoming zero-day exploit!",
        "budget": 10000,
        "targetValue": 100000,
        "assets": [
            {"id": "a1", "name": "Stateful Firewall", "cost": 5000, "defense": 60, "desc": "Blocks unsolicited traffic"},
            {"id": "a2", "name": "Intrusion Prevention (IPS)", "cost": 4000, "defense": 30, "desc": "Stops active exploits"},
            {"id": "a3", "name": "Basic Logging", "cost": 2000, "defense": 5, "desc": "Records but doesn't stop"}
        ],
        "options": ["High Security Portfolio (Firewall + IPS)", "Low Budget (Logging Only)"]
    },
    # Q6 — traffic_triage (Identifying ICMP Flood)
    {
        "local_id": 6, "format": "traffic_triage", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "DDoS Attacks — ICMP (Ping) Flood",
        "hint": "An ICMP 'Ping' is a simple check. If you receive 10,000 pings a second, someone is trying to crash your network. This is a Ping Flood.",
        "explain": "ICMP (Internet Control Message Protocol) is used for 'pings'. Malicious actors send huge volumes of pings to overwhelm your firewall's ability to process real web traffic. This is a basic 'Denial of Service' (DoS) attack.",
        "reveal": "BLOCK: IP 9.9.9.9! 10,000 ICMP packets per second is a clear attack. Legitimate traffic consists of varied TCP/UDP packets, not a wall of pings.",
        "correctAnswer": "BLOCK: IP 9.9.9.9",
        "questionText": "Network Storm! Your firewall is being hammered by pings. One source is sending 10,000 packets per second. Identify and BLOCK!",
        "files": [
            {"id": "R1", "name": "IP: 8.8.8.8 -> DNS Query (TCP 53)", "isMalware": False, "desc": "Normal DNS lookup"},
            {"id": "R2", "name": "IP: 9.9.9.9 -> ICMP ECHO REQUEST (x10,000/sec)", "isMalware": True, "desc": "Massive ICMP flood attack"}
        ]
    },

    # Q9 — click_flags (Firewall Log Audit)
    {
        "local_id": 9, "format": "click_flags", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "Detecting Data Exfiltration",
        "hint": "Look for a connection that has been active for 12 hours and has uploaded 100GB of data. That's not a normal webpage!",
        "explain": "Data exfiltration is the unauthorized transfer of data. It often happens over common ports like 443 (HTTPS) to blend in. Monitoring the 'Duration' and 'Total Bytes Sent' helps spot these long-lived connections.",
        "reveal": "Flagged! Connection to IP 45.33.22.11 uploaded 100GB. This is likely a database dump being stolen over an encrypted tunnel.",
        "correctFlags": ["f2"],
        "questionText": "Data Leak Hunt! Scan the outbound connections. Click the ONE connection that looks like a MASSIVE data theft in progress!",
        "emailParts": [
            {"id": "f1", "text": "Outbound: Google.com | Duration: 2m | Sent: 5MB", "isFlag": False},
            {"id": "f2", "text": "Outbound: 45.33.22.11 | Duration: 12h | Sent: 100GB (SUSPICIOUS)", "isFlag": True},
            {"id": "f3", "text": "Outbound: Microsoft Update | Duration: 15m | Sent: 500MB", "isFlag": False}
        ]
    },
    # Q10 — escape_rooms (Managing IP Tables)
    {
        "local_id": 10, "format": "escape_rooms", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "Basic Firewall Commands",
        "hint": "In a Linux terminal, 'iptables -A INPUT -s [IP] -j DROP' is the primary way to block a malicious IP manually.",
        "explain": "System administrators often use terminal commands for rapid response. Blocking a source IP at the kernel level (iptables) is faster than waiting for a GUI to load during a DDoS attack.",
        "reveal": "IP 8.8.8.8 has been dropped! You successfully used the command to shut down the offensive traffic stream.",
        "correctAnswer": "iptables -A INPUT -s 8.8.8.8 -j DROP",
        "questionText": "Terminal Defense! A malicious bot at 8.8.8.8 is flooding your server. Type the exact command to DROP all traffic from this IP!",
        "terminalOutput": [
            "[*] Incoming Flood: 8.8.8.8 -> Port 80 (10,000 req/sec)",
            "[*] Status: Server Overloaded",
            "[*] Type: iptables -A INPUT -s 8.8.8.8 -j DROP to stop it..."
        ]
    },
    # Q11 — traffic_triage (Tor Exit Node Detection)
    {
        "local_id": 11, "format": "traffic_triage", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "Anonymization Network Risks — Tor Exit Nodes",
        "hint": "Tor (The Onion Router) is used by hackers to hide their IP. If your firewall sees a connection from a 'Known Tor Exit Node', it's high risk.",
        "explain": "Tor is a legitimate privacy tool, but 90% of automated web attacks originate from its exit nodes. Many companies block Tor exit nodes by default to reduce 'Script Kiddie' noise.",
        "reveal": "BLOCK: IP 185.220.101.5. This is a known Tor Exit Node. Blocking it prevents anonymous scanners from mapping your site.",
        "correctAnswer": "BLOCK: IP 185.220.101.5",
        "questionText": "Privacy Audit! Your firewall flagged a known anonymous 'Tor Exit Node' trying to access your login page. Identify and BLOCK!",
        "files": [
            {"id": "T1", "name": "IP: 185.220.101.5 (Known TOR Exit Node)", "isMalware": True, "desc": "Anonymous source trying to scan /admin"},
            {"id": "T2", "name": "IP: 66.249.66.1 (Google Search Bot)", "isMalware": False, "desc": "Official crawler indexing your public pages"}
        ]
    },
    # Q12 — scenario_mcq (UPnP Risks)
    {
        "local_id": 12, "format": "scenario_mcq", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "UPnP (Universal Plug and Play) Security",
        "hint": "UPnP allows devices to automatically open ports on your firewall. This is convenient for Xbox, but DANGEROUS for security.",
        "explain": "UPnP was designed for home convenience, but malware uses it to 'Punch a hole' through your firewall from the inside. Always disable UPnP on corporate networks.",
        "reveal": "Disable UPnP entirely. It is a major security hole that lets internal malware open 'doors' to the outside world without your permission.",
        "questionText": "Configuration Audit! Should you enable 'UPnP' on your company's edge firewall to make joining Zoom calls easier?",
        "options": [
            "Yes — it automates port forwarding and saves time",
            "No — it allows internal devices to bypass security rules silently",
            "Yes — but only for the CEO's laptop"
        ],
        "correctAnswer": "No — it allows internal devices to bypass security rules silently"
    },
    # Q13 — sequence_builder (The 3-Way Handshake)
    {
        "local_id": 13, "format": "sequence_builder", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "TCP/IP Fundamentals — The 3-Way Handshake",
        "hint": "Before data flows, TCP needs to agree. The order is: SYN, SYN-ACK, ACK.",
        "explain": "Firewalls look at these flags. A 'SYN Flood' occurs when an attacker sends thousands of 'SYN' packets but never the final 'ACK', filling up the firewall's connection table.",
        "reveal": "Order: 1) SYN (Client requests), 2) SYN-ACK (Server agrees), 3) ACK (Client confirms). Data transfer only starts AFTER this sequence.",
        "questionText": "Protocol Architect! Arrange the TCP handshake packets in the correct order for a stateful firewall to allow them:",
        "steps": [
            {"id": "h1", "text": "SYN (Synchronize)", "correctOrder": 0},
            {"id": "h2", "text": "SYN-ACK (Synchronize-Acknowledge)", "correctOrder": 1},
            {"id": "h3", "text": "ACK (Acknowledge)", "correctOrder": 2}
        ]
    },
    # Q14 — traffic_triage (DNS Tunneling)
    {
        "local_id": 14, "format": "traffic_triage", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "Evasion Tactics — DNS Tunneling",
        "hint": "Check the DNS queries. If you see thousands of long, random queries to one domain like 'a1b2c3.evil.io', it's binary data hidden in text.",
        "explain": "DNS Tunneling bypasses firewalls because Port 53 (DNS) is almost always open. Attackers encode stolen data into the subdomains of their requests.",
        "reveal": "BLOCK: Query to evil.io. The massive volume of random subdomains indicates data exfiltration hidden as 'Domain Lookups'.",
        "correctAnswer": "BLOCK: x9z2p.evil.io",
        "questionText": "Sentry Duty! Your DNS logs show unusual activity. One internal PC is making 5,000 queries per minute to a weird domain. Block it!",
        "files": [
            {"id": "D1", "name": "Query: google.com (Type A)", "isMalware": False, "desc": "Normal web browsing"},
            {"id": "D2", "name": "Query: a62b1.x9z2p.evil.io (Type TXT - Massive volume)", "isMalware": True, "desc": "Potential DNS Tunneling detected"}
        ]
    },
    # Q15 — click_flags (Internal Lateral Movement)
    {
        "local_id": 15, "format": "click_flags", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "Internal Segmentation — Lateral Movement",
        "hint": "Why is the Marketing PC trying to connect to the HR Payroll Server via SMB (Port 445)? That's not part of the job!",
        "explain": "Internal firewalls stop hackers from moving 'sideways' (Lateral Movement) once they infect one PC. Segmentation ensures departments can't talk to each other's sensitive servers.",
        "reveal": "Flagged! Marketing_PC -> HR_Payroll on Port 445. This looks like a ransomware 'Worm' trying to spread to your most sensitive data.",
        "correctFlags": ["i2"],
        "questionText": "Internal Audit! Scan the traffic BETWEEN internal departments. Click the connection that looks like an attacker moving LATERALLY!",
        "emailParts": [
            {"id": "i1", "text": "Marketing_PC -> Marketing_File_Server (Port 445)", "isFlag": False},
            {"id": "i2", "text": "Marketing_PC -> HR_Payroll_Database (Port 445 - SUSPICIOUS)", "isFlag": True},
            {"id": "i3", "text": "IT_Admin -> Management_Switch (Port 22)", "isFlag": False}
        ]
    },
    # Q16 — decision_simulator (Application Layer vs Network Layer)
    {
        "local_id": 16, "format": "decision_simulator", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "L4 vs L7 Firewalls",
        "hint": "A 'Layer 4' (Network) firewall only sees IPs and Ports. A 'Layer 7' (Application) firewall can see the ACTUAL content of the message, such as 'SELECT * FROM users'.",
        "explain": "Modern threats hide inside secure ports (443). To stop them, you need 'Deep Packet Inspection' or a Web App Firewall (WAF) that operates at Layer 7.",
        "reveal": "Choose Layer 7 (Application Layer). It is the only way to inspect the content of HTTPS traffic and block SQL injections or malicious file uploads.",
        "questionText": "Architect Decision! You need to stop hackers from uploading viruses to your website via the 'Profile Pic' form. Which firewall type do you need?",
        "options": ["Layer 4 (IP/Port Blocking)", "Layer 7 (WAF / Application Inspection)", "Layer 3 (Router Only)"],
        "correctAnswer": "Layer 7 (WAF / Application Inspection)"
    },
    # Q17 — scenario_mcq (The Multi-Homed Risk)
    {
        "local_id": 17, "format": "scenario_mcq", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "Multi-Homed Hosts — Bypassing the Firewall",
        "hint": "If a server is connected to BOTH the internet AND the private internal network, it's called 'Multi-Homed'. It's a bridge for hackers.",
        "explain": "Hackers look for 'Dual-Homed' servers. If they compromise the web-facing side, they can use it as a 'Jump Box' to reach the internal database without hitting the main firewall.",
        "reveal": "Isolate the server. Use a DMZ (Demilitarized Zone) so the web server can talk to the internet OR the database, but NEVER acts as a direct bridge between them.",
        "questionText": "Security Briefing! A server is connected to the Public Web AND the Private Database LAN. This 'Bridge' is a massive risk. What is this server called?",
        "options": ["Dual-Homed / Multi-Homed Host", "Load Balancer", "Honeypot"],
        "correctAnswer": "Dual-Homed / Multi-Homed Host"
    },
    # Q18 — traffic_triage (Heartbleed-style Oversized Payloads)
    {
        "local_id": 18, "format": "traffic_triage", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "Packet Inspection — Anomaly Detection",
        "hint": "Check the payload size. A 'Heartbeat' packet should be 64 bytes. If it's 64,000 bytes, someone is trying to leak memory data.",
        "explain": "Protocols have expected sizes. Anomaly detection flags packets that are 'Malformed' or 'Oversized', which are common indicators of a buffer overflow or memory leak attack.",
        "reveal": "BLOCK: Request P2. The payload size of 64KB for a simple 'Is Alive' check is a clear attempt to trigger a memory leak.",
        "correctAnswer": "BLOCK: SSL Heartbeat (64KB)",
        "questionText": "Anomaly Audit! Your firewall flagged two SSL Heartbeat requests. One is normal, one is dangerously oversized. Block the threat!",
        "files": [
            {"id": "P1", "name": "SSL Heartbeat (64 Bytes)", "isMalware": False, "desc": "Standard keep-alive packet"},
            {"id": "P2", "name": "SSL Heartbeat (64 KB - SUSPICIOUS)", "isMalware": True, "desc": "Potential Heartbleed memory leak exploit"}
        ]
    },
    # Q19 — click_flags (Signs of a VPN Bypass)
    {
        "local_id": 19, "format": "click_flags", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "VPN Security — Shadow IT Detection",
        "hint": "Employees using 'Secret' VPNs to bypass your firewall blockages (like Gaming/TikTok sites) create unmonitored encrypted tunnels in your network.",
        "explain": "Shadow VPNs (like TunnelBear or Hotspot Shield) create an encrypted 'Pipe' that your firewall can't see into. This allows malware to enter your network without any inspection.",
        "reveal": "Flagged! Generic VPN Traffic on Port 1194. This is an unapproved encrypted tunnel. All traffic should go through the official Corporate VPN only.",
        "correctFlags": ["v2"],
        "questionText": "Shadow IT Audit! Find the connection attempting to bypass the firewall rules using an unauthorized personal VPN!",
        "emailParts": [
            {"id": "v1", "text": "Outbound: Office365.com (Port 443)", "isFlag": False},
            {"id": "v2", "text": "Outbound: Unnamed_VPN_Proxy (Port 1194 - SUSPICIOUS)", "isFlag": True},
            {"id": "v3", "text": "Outbound: Zoom Video (Port 8801)", "isFlag": False}
        ]
    },
    # Q20 — escape_rooms (Analyzing Logs with Grep)
    {
        "local_id": 20, "format": "escape_rooms", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "Log Analysis with CLI",
        "hint": "Use 'grep' to search logs. 'grep \"DENY\" firewall.log' will show you everything your firewall has blocked.",
        "explain": "Filtering large logs is key. 'grep' allows you to find specific patterns (like an IP or Error code) in seconds, rather than scrolling through millions of lines.",
        "reveal": "Search Complete! You found 500 DENY entries for IP 77.77.77.77. This IP is definitely an attacker scanning for vulnerabilities.",
        "correctAnswer": "grep \"DENY\" firewall.log",
        "questionText": "CLI Forensic! You have a massive firewall.log file. Type the command to find all occurrences of the word 'DENY'!",
        "terminalOutput": [
            "[*] firewall.log size: 5.2 GB",
            "[*] Total lines: 14,000,000",
            "[*] Type: grep \"DENY\" firewall.log to filter results..."
        ]
    },
    # Q21 — scenario_mcq (Egress Filtering Philosophy)
    {
        "local_id": 21, "format": "scenario_mcq", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "Egress vs Ingress Filtering",
        "hint": "Ingress is traffic coming IN. Egress is traffic going OUT. Most companies forget to block traffic going out, which is how malware 'Calls Home'.",
        "explain": "Egress filtering is vital. If a server is only supposed to talk to Google, block it from talking to anything else. This prevents infected servers from connecting to a hacker's C2 server.",
        "reveal": "Implement Egress Filtering. By blocking all outbound traffic except specifically approved destinations, you cripple malware's ability to 'Call Home' or exfiltrate data.",
        "questionText": "Advanced Strategy! You have a perfect 'Inbound' firewall. Your boss says: 'Why do we need to block traffic going OUT?' What is your best answer?",
        "options": [
            "We don't — our users are trustworthy",
            "To prevent infected devices from 'Calling Home' to C2 servers",
            "To save bandwidth on the upload side"
        ],
        "correctAnswer": "To prevent infected devices from 'Calling Home' to C2 servers"
    },
    # Q22 — traffic_triage (Identifying Botnet Beaconing)
    {
        "local_id": 22, "format": "traffic_triage", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "Botnet Detection — Beaconing Patterns",
        "hint": "Look for a client that sends exactly 50 bytes every 60 seconds, 24/7. This 'Heartbeat' is a bot checking for orders.",
        "explain": "Beaconing is a 'Pulse'. It doesn't use much data, but its extreme consistency over days reveals an automated bot script waiting for instructions from its master.",
        "reveal": "BLOCK: IP 101.55.22.4. The 'Pulse' of 60-second intervals is a classic botnet beacon. This PC is infected and waiting for a command to start a DDoS.",
        "correctAnswer": "BLOCK: Beacon IP 101.55.22.4",
        "questionText": "Persistence Audit! Your network analyzer shows a 'Pulse' from one internal PC. It connects every 60 seconds exactly. Identify the Beacon!",
        "files": [
            {"id": "B1", "name": "PC_1 -> Google (Random intervals)", "isMalware": False, "desc": "Normal user search behavior"},
            {"id": "B2", "name": "PC_1 -> 101.55.22.4 (EXACT 60s Interval)", "isMalware": True, "desc": "Malicious beacon pulse detected"}
        ]
    },
    # Q23 — scenario_mcq (Defense in Depth)
    {
        "local_id": 23, "format": "scenario_mcq", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "Security Architecture — Defense in Depth",
        "hint": "A single firewall is not enough. You need layers: Edge Firewall, Internal Firewall, Host-based Firewall, and Antivirus.",
        "explain": "Defense in Depth assumes the first layer WILL fail. If a hacker passes the edge, they still have to beat the internal segment and the local PC's security.",
        "reveal": "Layers are key. Security is about slowing the attacker down and creating multiple chances to detect them. Never rely on a single 'Gate' to protect everything.",
        "questionText": "Architecture Audit! Your boss says: 'We have a $50k edge firewall, so we can turn off the firewalls on individual laptops to save CPU.' Correct?",
        "options": [
            "Yes — the edge firewall stops everything anyway",
            "No — we need 'Defense in Depth' (Layers) in case the edge is bypassed",
            "Yes — host-based firewalls are obsolete"
        ],
        "correctAnswer": "No — we need 'Defense in Depth' (Layers) in case the edge is bypassed"
    },
    # Q24 — click_flags (SSL Inspection Risks)
    {
        "local_id": 24, "format": "click_flags", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "SSL/TLS Inspection (Deep Packet Inspection)",
        "hint": "Hackers hide malware inside encrypted HTTPS traffic. To stop them, you must 'Break' the encryption, inspect it, then re-encrypt it. This is 'SSL Inspection'.",
        "explain": "Without SSL/TLS Inspection, your firewall is 'Blind'. It sees Port 443 traffic but has no idea if it's a Cat Video or a Ransomware payload. This is a trade-off between privacy and security.",
        "reveal": "Flag 'Blind Spot'! 443 traffic without inspection is a tunnel for malware. Always implement SSL Inspection for corporate devices to maintain visibility into threats.",
        "correctFlags": ["s1"],
        "questionText": "Visibility Audit! Your firewall says: 'Encrypted Traffic (443) — CONTENT UNKNOWN'. Click the dangerous visibility blind spot!",
        "emailParts": [
            {"id": "s1", "text": "HTTPS Content: [HIDDEN / BLIND SPOT] (NO SSL INSPECTION)", "isFlag": True},
            {"id": "s2", "text": "HTTP Content: [VISIBLE] (Inspected)", "isFlag": False},
            {"id": "s3", "text": "DNS Content: [VISIBLE] (Inspected)", "isFlag": False}
        ]
    },

    # Q7 — select_all (Signs of Port Scanning)
    {
        "local_id": 7, "format": "select_all", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "Identifying Reconnaissance — Port Scanning",
        "hint": "Before a hacker attacks, they 'scan' your ports. You will see a sequence of connection attempts to every port (1, 2, 3...) in a very short time.",
        "explain": "A port scan is like a thief checking every door and window in your house. Indicators: connection attempts to every port from 1 to 1024, 'Half-Open' (SYN) scans that never finish the connection, and all attempts originating from one external IP.",
        "reveal": "All 4 are signs! 🔍 Sequence of ports, ⚡ High speed, 👤 One IP address, and 🌉 'Half-open' connections. If you detect this, you should 'Block and Alert' before the actual exploit starts.",
        "correctAnswer": "Select all 4: Port sequence, High speed, Single IP, Half-open SYN",
        "questionText": "Recon Sentry! Your logs show a 'Survey' attack. Select ALL the indicators that someone is Port Scanning your network:",
        "options": [
            "Sequential connection attempts to ports 21, 22, 23, 25, 80, 443...",
            "Attempts occur at a rate of 500 ports per second",
            "All connection attempts are coming from the same external IP address",
            "Connections are 'SYN' only — they never complete the 3-Way Handshake",
            "One user is downloading a large file on Port 443"
        ],
        "correctFlags": [
            "Sequential connection attempts to ports 21, 22, 23, 25, 80, 443...",
            "Attempts occur at a rate of 500 ports per second",
            "All connection attempts are coming from the same external IP address",
            "Connections are 'SYN' only — they never complete the 3-Way Handshake"
        ]
    },

    # Q8 — decision_simulator (Stateful vs Stateless)
    {
        "local_id": 8, "format": "decision_simulator", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "Firewall Technology — Stateful Inspection",
        "hint": "A 'Stateful' firewall remembers that you asked for a website, so it lets the reply back in automatically. A 'Stateless' firewall checks every single packet without any memory of the past. Which is more secure and efficient?",
        "explain": "Stateful inspection tracks the 'State' of network connections (the 3-Way Handshake). It knows if a packet is part of an existing 'Safe' conversation or a new, unsolicited 'Attack' attempt. Stateless firewalls are easily tricked by hackers faking a 'Reply' packet.",
        "reveal": "Choose Stateful Inspection. It is vastly more secure because it understands context. It won't let a 'Reply' packet in unless there was an original 'Request' from inside your network.",
        "questionText": "Arch Briefing! You are buying a new firewall. The vendor offers a 'Stateless Packet Filter' and a 'Stateful Inspection Firewall'. Which do you choose for better security?",
        "options": [
            "Stateless — it's faster because it doesn't have to remember anything",
            "Stateful — it tracks active connections and blocks unsolicited replies",
            "Both are identical in modern security protection"
        ],
        "correctAnswer": "Stateful — it tracks active connections and blocks unsolicited replies"
    },

    # Q25 — decision_simulator (Geo-blocking)
    {
        "local_id": 25, "format": "decision_simulator", "difficulty": "medium",
        "gameName": "firewall", "game_key": "firewall", "level_name": "medium",
        "concept": "Geo-Blocking Policy",
        "hint": "If you have zero customers in a specific country, block that country's traffic to reduce bot noise.",
        "reveal": "Geo-blocking is a massive 'Noise Filter'. It stops 90% of automated botnet traffic that isn't using a local proxy, reducing log fatigue.",
        "questionText": "Noise Filter! 90% of your web errors come from a country where you have ZERO customers. Solution?",
        "options": [
            "Increase bandwidth",
            "Implement a Geo-IP Firewall rule to block that country",
            "Ignore it — they don't have a password"
        ],
        "correctAnswer": "Implement a Geo-IP Firewall rule to block that country"
    }
]

# Note: Final script will contain exactly 25.
result = col.insert_many(questions)
print(f"Inserted {len(result.inserted_ids)} unique Firewall Medium missions.")
client.close()
