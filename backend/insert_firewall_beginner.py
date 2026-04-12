from dotenv import load_dotenv
import os
load_dotenv()
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGO_URI'))
col = client['cyberduo']['questions']

# Clear any existing firewall beginner questions
col.delete_many({'game_key': 'firewall', 'level_name': 'beginner'})

questions = [

    # Q1 — scavenger_hunt (Laser Grid: Connect Devices)
    # Themed around: "Laser Grid" Connect — draw firewall across 5 devices
    {
        "local_id": 1, "format": "scavenger_hunt", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "What a Firewall Protects",
        "hint": "A firewall works best when it stands between ALL devices and the outside internet. Click every device that NEEDS to be placed behind the firewall laser grid!",
        "explain": "A firewall is like an invisible electric fence around your devices. For it to work, EVERY device on your network — laptops, phones, printers, smart TVs — must be placed behind it. If even ONE device skips the firewall, the whole network has a gap that hackers can walk through!",
        "reveal": "You needed to place the Laptop, Office PC, Smart Printer, and Wi-Fi Router behind the Firewall Laser Grid. The ONLY device left outside is the public-facing web server (which needs special rules of its own). Every internal device must sit behind the firewall wall!",
        "correctAnswer": "Click: Laptop, Office PC, Smart Printer, Wi-Fi Router — all must sit behind the firewall!",
        "questionText": "Laser Grid Challenge! Five devices are on screen. Draw your Firewall 'Laser Line' to protect the right ones. Click ALL the devices that should be placed BEHIND the firewall to keep them safe from the internet!",
        "objects": [
            {"id": "o1", "icon": "💻", "label": "Laptop — connects to internet daily", "isRedFlag": True, "top": "12%", "left": "8%"},
            {"id": "o2", "icon": "🖥️", "label": "Office PC — stores company files", "isRedFlag": True, "top": "12%", "left": "55%"},
            {"id": "o3", "icon": "🖨️", "label": "Smart Printer — connected to local network", "isRedFlag": True, "top": "50%", "left": "30%"},
            {"id": "o4", "icon": "📡", "label": "Wi-Fi Router — gateway to all devices", "isRedFlag": True, "top": "75%", "left": "8%"},
            {"id": "o5", "icon": "🌐", "label": "Public Web Server — serves the company website to everyone", "isRedFlag": False, "top": "75%", "left": "60%"}
        ]
    },

    # Q2 — traffic_triage (Pressure Valve Control: Allow or Block Traffic)
    # Themed around: "Pressure Valve Control" — throttle bad traffic, keep good traffic
    {
        "local_id": 2, "format": "traffic_triage", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Allowing and Blocking Network Traffic",
        "hint": "Work traffic goes to known, trusted websites like office tools. Unknown traffic going to strange IP addresses with no clear reason should be BLOCKED!",
        "explain": "A firewall acts like a Pressure Valve on a water pipe — it controls what flows through your network. Normal work traffic (browsing company tools, sending emails) should flow freely. Unknown traffic to suspicious addresses should be throttled and blocked before it causes damage or leaks data.",
        "reveal": "ALLOW: Office365 connection (legitimate work tool) and Google search traffic (normal browsing). BLOCK: The unknown IP 185.220.0.1 sending large data packets (could be data theft!) and the connection to 'darkmarket.onion' (a dark web address — no legitimate business uses .onion from an office!).",
        "correctAnswer": "ALLOW: office365.com, google.com — BLOCK: 185.220.0.1 (unknown large upload), darkmarket.onion",
        "questionText": "Pressure Valve Control! Your network pipe is filling up with both Work Traffic and Unknown Traffic. Sort each connection — ALLOW it through or BLOCK it at the firewall valve!",
        "files": [
            {"id": "f1", "icon": "💼", "name": "office365.com — Employee sending work emails", "isMalware": False},
            {"id": "f2", "icon": "🌐", "name": "google.com — Employee doing a Google search", "isMalware": False},
            {"id": "f3", "icon": "⚠️", "name": "185.220.0.1 — Unknown IP receiving large file upload from your PC", "isMalware": True},
            {"id": "f4", "icon": "💀", "name": "darkmarket.onion — Dark web connection request from office PC", "isMalware": True}
        ]
    },

    # Q3 — decision_simulator (Shield-Bash Reaction: Attack on a port)
    # Themed around: "Shield-Bash" Reaction — attack orbs hit server from different angles
    {
        "local_id": 3, "format": "decision_simulator", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Responding to a Port Attack",
        "hint": "When a known dangerous port is being hammered by suspicious traffic, the FIREWALL is your shield — use it to block ONLY that port immediately!",
        "explain": "Hackers often attack specific 'doors' into your server called Ports. Each port lets a different service through. Port 23 (Telnet) is especially dangerous because it is old, unencrypted, and should almost never be open. When you see repeated suspicious access attempts, firewalling that port is the fastest way to stop the attack!",
        "reveal": "Blocking Port 23 (Telnet) immediately is the correct Shield-Bash! Telnet sends data in plain text — hackers can read everything. Most modern networks should have Telnet completely blocked. Ignoring it or just logging out lets the attacker keep trying. Shutting down the whole server disrupts legitimate users unnecessarily.",
        "questionText": "Shield-Bash! Your server dashboard is flashing RED — an attacker is hammering Port 23 (Telnet) with hundreds of login attempts per minute! What is the correct Shield-Bash response?",
        "options": [
            "Ignore it — the server's password is strong so it probably cannot be broken",
            "Immediately block Port 23 at the firewall to stop all traffic on that vulnerable port",
            "Shut down the entire server — better safe than sorry even if it disrupts all users",
            "Just log out of the server admin panel — the attacker will give up eventually"
        ],
        "correctAnswer": "Immediately block Port 23 at the firewall to stop all traffic on that vulnerable port"
    },

    # Q4 — sequence_builder (Port Key-Code: Lock ports in correct order)
    # Themed around: "The Port Key-Code" — click ports in sequence to lock them
    {
        "local_id": 4, "format": "sequence_builder", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Understanding Common Network Ports",
        "hint": "Think about what each port is used for: web browsing first, then secure browsing, then admin access last. Lock them in order of how a hacker would try to enter!",
        "explain": "Ports are numbered entry points into a computer. Port 80 is regular web traffic, Port 443 is secure (HTTPS) web traffic, and Port 22 is SSH (remote server access). Hackers probe ports in order — understanding this sequence helps you lock them in the right priority when under attack!",
        "reveal": "Correct lock sequence: 1) Port 22 (SSH — direct server admin access, highest risk!), 2) Port 21 (FTP — file transfer, commonly exploited), 3) Port 80 (HTTP — unencrypted web, medium risk), 4) Port 443 (HTTPS — encrypted web, lowest risk of the four). Lock the most dangerous access points first!",
        "questionText": "Port Key-Code! A hacker is knocking on four ports. You must lock them from MOST DANGEROUS to LEAST DANGEROUS. Arrange them in the correct security priority order!",
        "steps": [
            {"id": "s1", "text": "Port 22 — SSH: Direct remote admin access to the server", "correctOrder": 0},
            {"id": "s2", "text": "Port 21 — FTP: File transfer protocol, often unencrypted", "correctOrder": 1},
            {"id": "s3", "text": "Port 80 — HTTP: Regular unencrypted web browsing traffic", "correctOrder": 2},
            {"id": "s4", "text": "Port 443 — HTTPS: Encrypted web traffic, most secure of the four", "correctOrder": 3}
        ]
    },

    # Q5 — scenario_mcq (Signal Jammer: Spy Satellite beaming data out)
    # Themed around: "Signal Jammer" — stop a spy satellite data beam
    {
        "local_id": 5, "format": "scenario_mcq", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Blocking Unauthorised Data Outflow",
        "hint": "The data is leaving your network without permission. A firewall's OUTBOUND rules are designed exactly to stop this — think about which tool controls what LEAVES your network!",
        "explain": "Most people think firewalls only block things coming IN. But firewalls also control what goes OUT! Outbound firewall rules can detect and block applications secretly sending your company's data to the internet — exactly like jamming a spy satellite signal before it escapes.",
        "reveal": "Outbound firewall rules are the correct 'signal jammer'! By monitoring and blocking suspicious outgoing connections, a firewall stops data from being secretly transmitted to an attacker's server. Antivirus scans for malware files, Wi-Fi passwords stop people logging in, and secure passwords protect accounts — but NONE of these stop outbound data theft.",
        "questionText": "Signal Jammer! An unknown app on your company laptop is secretly beaming data out to an unfamiliar server — like a spy satellite! Which security tool acts as a 'Signal Jammer' to block this outgoing leak?",
        "options": [
            "Set a stronger Wi-Fi password — makes the network harder to join from outside",
            "Configure Outbound Firewall Rules to detect and block unauthorised data leaving the network",
            "Run an antivirus scan — the antivirus will detect the outgoing connection",
            "Change your account password — stops hackers from logging into your account"
        ],
        "correctAnswer": "Configure Outbound Firewall Rules to detect and block unauthorised data leaving the network"
    },

    # Q6 — click_flags (Encrypted Maze: Find open dangerous paths / firewall switch settings)
    # Themed around: "Encrypted Maze" — click the wrong firewall switches
    {
        "local_id": 6, "format": "click_flags", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Spotting Dangerous Firewall Rule Configurations",
        "hint": "Safe firewall rules are SPECIFIC and LIMITED. Dangerous rules are the ones that say 'Allow ALL' or use wildcards — these punch holes in your firewall wall!",
        "explain": "In the Encrypted Maze, setting a firewall switch to the wrong position opens a path for Sniffer Bots. In real life, overly permissive firewall rules — like 'Allow ALL on Port 80' or 'Accept from ANY IP' — are the most dangerous settings because they let almost anything through, making the whole firewall useless!",
        "reveal": "The two dangerous switches: 'Allow ALL inbound traffic on Port 80 from ANY IP address' (this lets everyone through, not just legitimate users!) and 'Accept connections from ANY source on Port 22' (this opens SSH to the entire internet — hackers love this!). The other two rules are properly restricted and safe.",
        "correctAnswer": "Click the two dangerous switches: Allow ALL on Port 80 from ANY, and Accept ANY source on Port 22",
        "questionText": "Encrypted Maze! Your firewall has four rule switches. Two are dangerously wrong and will let Sniffer Bots through. Click ALL the switches that are configured BADLY and need to be fixed!",
        "emailParts": [
            {"id": "p1", "text": "SWITCH A: Allow inbound traffic on Port 443 from office IP range only (192.168.1.x)", "isFlag": False},
            {"id": "p2", "text": "SWITCH B: Allow ALL inbound traffic on Port 80 from ANY IP address in the world", "isFlag": True},
            {"id": "p3", "text": "SWITCH C: Block all incoming traffic on Port 23 (Telnet) — permanently closed", "isFlag": False},
            {"id": "p4", "text": "SWITCH D: Accept connections from ANY source on Port 22 (SSH remote admin)", "isFlag": True}
        ],
        "correctFlags": ["p2", "p4"]
    },

    # Q7 — file_triage (Deep Packet Scanner: Sort data packets — safe or devil)
    # Themed around: "Deep Packet Scanner (X-Ray)" — x-ray boxes on belt
    {
        "local_id": 7, "format": "file_triage", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Deep Packet Inspection Basics",
        "hint": "Normal data packets go to familiar websites and carry expected data types. Suspicious packets go to unknown IPs, carry unexpected content, or try to hide what they are!",
        "explain": "Deep Packet Inspection (DPI) is when a firewall looks INSIDE each data packet — not just who it's addressed to, but what is IN it. This is like X-raying luggage at an airport. Normal packets have an obvious harmless purpose. Suspicious ones try to sneak past by pretending to be something they are not!",
        "reveal": "SUSPICIOUS (toss off the belt!): The packet pretending to be 'photo.jpg' but actually containing executable code — files cannot change type like this! Also the packet to 192.168.99.99 sending encrypted SQL commands at 3AM — that is clearly data theft in progress. SAFE: The regular HTTPS web request and the normal email sending packet.",
        "correctAnswer": "BLOCK: fake photo packet with hidden code, and 3AM SQL data packet. ALLOW: HTTPS web, normal email",
        "questionText": "Deep Packet Scanner! Data packets are moving through your network like boxes on a conveyor belt. X-Ray each one — mark it SAFE (ALLOW) or SUSPICIOUS (BLOCK) before it gets through!",
        "files": [
            {"id": "f1", "icon": "🌐", "name": "HTTPS request to google.com — Employee browsing web securely", "isMalware": False},
            {"id": "f2", "icon": "💀", "name": "Packet labelled 'photo.jpg' but contains executable code hidden inside", "isMalware": True},
            {"id": "f3", "icon": "📧", "name": "Email to colleague@company.com — normal text email sending", "isMalware": False},
            {"id": "f4", "icon": "💀", "name": "3AM packet to 192.168.99.99 sending encrypted SQL database dump", "isMalware": True}
        ]
    },

    # Q8 — select_all (Wall Builder Speed-Run: Choose the right firewall components)
    # Themed around: "The Wall Builder Speed-Run" — choose correct firewall bricks
    {
        "local_id": 8, "format": "select_all", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "What Makes a Good Firewall Setup",
        "hint": "Strong firewall 'bricks' are things that ACTIVELY filter, monitor, or control traffic. Weak bricks are things that don't actually check network connections at all!",
        "explain": "A solid firewall 'wall' is built from several layers of protection working together. Just like a wall needs strong bricks to hold up, a firewall setup needs the right components — rules, monitoring, and updates. Using weak components (like only a basic password) leaves your wall full of holes that Malware Rain can dissolve!",
        "reveal": "The 4 strong firewall bricks: Inbound/outbound traffic rules (core function!), Real-time traffic monitoring (catches threats live), Regular firewall rule updates (keeps rules current), and Blocking unused ports (removes unnecessary entry points). WEAK bricks: A strong Wi-Fi password alone does NOT make a firewall — and turning off your PC is not a security strategy!",
        "correctAnswer": "Choose: traffic rules, real-time monitoring, regular updates, blocking unused ports",
        "questionText": "Wall Builder Speed-Run! Build your Firewall Wall using the strongest bricks. Select ALL the components that genuinely make a firewall stronger and more secure:",
        "options": [
            "Creating specific Inbound and Outbound traffic rules for each service",
            "Setting a very strong Wi-Fi password (this helps network access, not firewall strength itself)",
            "Enabling Real-Time traffic monitoring to detect threats as they happen",
            "Regularly updating firewall rules to block newly discovered attack patterns",
            "Turning off your computer at night (a firewall must run 24/7 to protect you!)",
            "Blocking all unused network ports that no service needs open"
        ],
        "correctFlags": [
            "Creating specific Inbound and Outbound traffic rules for each service",
            "Enabling Real-Time traffic monitoring to detect threats as they happen",
            "Regularly updating firewall rules to block newly discovered attack patterns",
            "Blocking all unused network ports that no service needs open"
        ]
    },

    # Q9 — the_imposter (Trust Meter: Find the unverified device trying to connect)
    # Themed around: "The Trust Meter Tug-of-War" — keep tapping Verify on stranger device
    {
        "local_id": 9, "format": "the_imposter", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Network Access Control — Trusting Devices",
        "hint": "The suspicious device is the one connecting from a totally UNKNOWN location with no good reason to be on the network. Which device's story does NOT add up?",
        "explain": "Firewalls and Network Access Control systems check if connecting devices should be trusted before letting them in. Just like a bouncer at a club checking IDs, if a device cannot prove it belongs on your network, it should be blocked — even if it 'looks' like a normal laptop. Unverified devices let hackers sneak in!",
        "reveal": "The suspicious device is the 'Unknown Laptop from IP 185.23.11.99 in Russia'! Your company has no offices in Russia and no contractor was authorised. The Office PC and Manager's Phone are both familiar, known, and have a clear reason for being on the network. Unknown devices must be blocked until verified!",
        "questionText": "Trust Meter Tug-of-War! Three devices are trying to connect to your company network. One is a stranger that cannot be trusted. Find the imposter you should BLOCK before it slips through the firewall!",
        "messages": [
            {"sender": "Office-PC-01", "text": "Connection request from PC-01 — standard office workstation, registered device, Location: Head Office, UK", "isPhish": False},
            {"sender": "Unknown-Laptop", "text": "Connection request from unregistered laptop — Location: Russia (IP: 185.23.11.99), no authorised contractor login, requesting admin access", "isPhish": True},
            {"sender": "Manager-iPhone", "text": "Connection request from Manager Sarah's iPhone — registered mobile device, Location: Office Wi-Fi network, UK", "isPhish": False}
        ],
        "options": ["Office-PC-01", "Unknown-Laptop", "Manager-iPhone"],
        "correctAnswer": "Unknown-Laptop"
    },

    # Q10 — spot_fake (Shadow Filter: Shadow has spikes = virus, round = safe)
    # Themed around: "The Shadow Filter" — see shadow of packet, classify it
    {
        "local_id": 10, "format": "spot_fake", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Recognising Dangerous vs Safe Data Packets",
        "hint": "Safe packets have a clear, expected purpose and go to familiar destinations. A 'spiky' suspicious packet has something odd about it — unusual port, unknown destination, or weird timing!",
        "explain": "In real networking, firewalls use rules to classify passing data like the Shadow Filter. Packets with 'spikes' — suspicious patterns like unknown destinations, odd ports, or unexpected timing — get hard-blocked. Round, expected, normal-looking packets are allowed through. This is the foundation of how all modern firewalls work!",
        "reveal": "The SUSPICIOUS packet is the one connecting to Port 4444 from an unknown external IP! Port 4444 is a well-known hacker backdoor port associated with the Metasploit attack tool. Normal data like web traffic sits on Port 443 or Port 80. Anything connecting on Port 4444 at midnight to an unknown external server is almost certainly a remote access trojan phoning home!",
        "questionText": "Shadow Filter! You see the shadow of an incoming data packet BEFORE it arrives. One of these packets has 'spikes' and is clearly dangerous. Which one should you HARD BLOCK before it enters?",
        "options": [
            "Packet A: HTTPS connection from employee's laptop to office365.com on Port 443 at 9am",
            "Packet B: Incoming connection to Port 4444 from unknown external IP 91.234.11.33 at midnight",
            "Packet C: Email from colleague@company.com sent on Port 25 (standard mail) at 2pm",
            "Packet D: DNS lookup from office router to google.com on Port 53 at 11am"
        ],
        "correctAnswer": "Packet B: Incoming connection to Port 4444 from unknown external IP 91.234.11.33 at midnight"
    },

    # Q11 — sequence_builder (Circuit Repair: Restore firewall in correct order)
    # Themed around: "Firewall Circuit Repair" — drag chips into slots in correct order
    {
        "local_id": 11, "format": "sequence_builder", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Setting Up a Firewall Correctly",
        "hint": "Think logically — you cannot write rules before installing the firewall. You cannot test before turning it on. What must come first to avoid 'overheating'?",
        "explain": "Setting up a firewall is like repairing a circuit board — each chip must go in the correct slot or the whole system fails. Security teams follow a clear order: install first, configure rules second, enable monitoring third, test fourth, and document everything last so the team knows what is running!",
        "reveal": "Correct repair order: 1) Install firewall software/hardware (you need the tool first!), 2) Configure inbound and outbound traffic rules (define what is allowed), 3) Enable logging and monitoring (so you can see what is happening), 4) Test the firewall with safe test traffic (verify it works), 5) Document all rules for the IT team (so everyone knows the setup). Missing any step creates a broken circuit!",
        "questionText": "Circuit Repair! The office firewall has crashed and needs rebuilding from scratch. Drag the Security Chips into the correct slots — arrange these 5 setup steps in the RIGHT ORDER to restore the firewall!",
        "steps": [
            {"id": "s1", "text": "Install the firewall software or hardware on the network gateway", "correctOrder": 0},
            {"id": "s2", "text": "Configure inbound and outbound traffic filtering rules for all services", "correctOrder": 1},
            {"id": "s3", "text": "Enable traffic logging and real-time monitoring alerts", "correctOrder": 2},
            {"id": "s4", "text": "Test the firewall by running safe test traffic through all rules", "correctOrder": 3},
            {"id": "s5", "text": "Document all firewall rules for the IT team's records", "correctOrder": 4}
        ]
    },

    # Q12 — scavenger_hunt (Ghost in the Machine: Find the ghost user account)
    # Themed around: "Ghost in the Machine Hunt" — find the flickering ghost account
    {
        "local_id": 12, "format": "scavenger_hunt", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Identifying Unauthorised User Accounts",
        "hint": "Look for accounts that have no clear owner, were created at a suspicious time, have not been used in a very long time, or have a suspiciously generic name. These are the ghost accounts!",
        "explain": "Hackers often create hidden 'ghost accounts' on networks — these are user accounts with no obvious owner that give them a secret back door to return later. Regular account audits are an important part of network security. Finding and disabling accounts that should not exist is like removing a ghost from the machine!",
        "reveal": "The ghost accounts are 'admin_backup' (created at 2AM by an unknown source — no IT team creates admin accounts at 2AM!) and 'user_temp_99' (has not been used for 847 days and has no assigned owner — a textbook abandoned ghost account used by hackers). Regular users like Sarah, James, and IT-Helpdesk are all normal verified accounts.",
        "correctAnswer": "Click: admin_backup (created 2AM, unknown) and user_temp_99 (867 days unused, no owner)",
        "questionText": "Ghost Hunt! The system shows all active user accounts. Some accounts have no real owner and are flickering with ghostly activity. Find ALL the suspicious ghost accounts and click them to Revoke Access before the timer runs out!",
        "objects": [
            {"id": "o1", "icon": "👤", "label": "sarah.jones@company.com — Marketing Team, Last login: Today", "isRedFlag": False, "top": "12%", "left": "8%"},
            {"id": "o2", "icon": "👻", "label": "admin_backup — Created: 2AM last Tuesday, Creator: UNKNOWN SOURCE", "isRedFlag": True, "top": "12%", "left": "55%"},
            {"id": "o3", "icon": "👤", "label": "james.smith@company.com — Finance Team, Last login: Yesterday", "isRedFlag": False, "top": "50%", "left": "8%"},
            {"id": "o4", "icon": "👻", "label": "user_temp_99 — Owner: Unassigned, Last login: 847 days ago", "isRedFlag": True, "top": "50%", "left": "55%"},
            {"id": "o5", "icon": "🛠️", "label": "IT-Helpdesk — IT Admin account, Last login: 2 hours ago", "isRedFlag": False, "top": "80%", "left": "30%"}
        ]
    },

    # Q13 — branching_narratives (Inbound vs Outbound Seesaw: Balance the traffic)
    # Themed around: "The Inbound vs Outbound Seesaw"
    {
        "local_id": 13, "format": "branching_narratives", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Inbound vs Outbound Firewall Rules",
        "hint": "The question is whether the data is coming INTO the network or going OUT. Most firewalls block dangerous incoming and also monitor unexpected outgoing. Which rule fixes the imbalance?",
        "explain": "A firewall seesaw has two sides: INBOUND (traffic coming into your network from the internet) and OUTBOUND (traffic leaving your network to the internet). Both sides need rules! Too much unrestricted inbound traffic means hackers can get in. Too much unrestricted outbound traffic means your data might be leaking out without you knowing.",
        "reveal": "The correct action is to add a specific Outbound Rule blocking unknown destinations! If a large amount of your private data is going OUT to unknown servers — that is a data leak or data theft in progress. You need to add an outbound rule immediately to stop it. Simply blocking all inbound traffic would break normal browsing and is too broad.",
        "questionText": "Seesaw Alert! Your firewall dashboard shows the Outbound side is dangerously heavy — large amounts of private company data are flowing OUT to unknown servers. What is the correct action to rebalance the seesaw?",
        "options": [
            "Block ALL inbound traffic completely — this will stop hackers from sending commands",
            "Add a specific Outbound Rule restricting which servers your company data is allowed to be sent to",
            "Add no new rules — outbound traffic is always safe because it is going OUT, not IN"
        ],
        "correctAnswer": "Add a specific Outbound Rule restricting which servers your company data is allowed to be sent to"
    },

    # Q14 — scenario_mcq (VPN Tunnel: Choose correct safe path to office server)
    # Themed around: "The VPN Tunnel Dig" — dig a tunnel avoiding hackers
    {
        "local_id": 14, "format": "scenario_mcq", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "What a VPN Does and Why It Matters",
        "hint": "A VPN creates a private encrypted tunnel through the dangerous public internet — like a secret underground passage that hackers above ground cannot see into. Which option describes this correctly?",
        "explain": "When you work remotely and connect to the company server over the public internet, your data travels through many routers that could be owned by anyone — including hackers. A VPN (Virtual Private Network) digs an encrypted tunnel that hides and protects your data as it travels, so even if a hacker intercepts it, they see only scrambled nonsense!",
        "reveal": "A VPN encrypts all traffic between your home laptop and the office server — this is the correct tunnel! Without a VPN, data travels in the open across the public internet where any 'Dirt Clump' hacker with the right tools can intercept it. Just having a strong password or using HTTPS for some sites does not protect ALL your network traffic — only a VPN does that.",
        "questionText": "VPN Tunnel Dig! You are working from home and need to safely reach your company's Office Server across the dangerous Public Internet. Which tool digs the safest encrypted tunnel, avoiding all the Hackers (Dirt Clumps) lurking in the public network?",
        "options": [
            "Browser incognito mode — hides your browsing from websites and other people on your PC",
            "A VPN (Virtual Private Network) — creates an encrypted tunnel between your device and the office server",
            "A strong Wi-Fi password — prevents others from joining your home Wi-Fi network",
            "Using HTTPS websites — only encrypts the specific website connection, not all your traffic"
        ],
        "correctAnswer": "A VPN (Virtual Private Network) — creates an encrypted tunnel between your device and the office server"
    },

    # Q15 — click_flags (Bouncer Eye-Spy: Block specific bad IP addresses in crowd)
    # Themed around: "The Bouncer Eye-Spy" — block all red hat IPs in crowd
    {
        "local_id": 15, "format": "click_flags", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "IP Address Blocking with Firewall Rules",
        "hint": "The firewall Bouncer has been told to block a specific IP range: 45.33.x.x — these are the 'Red Hats'. Click ONLY the connection requests coming from this range!",
        "explain": "A firewall can act like a Bouncer that blocks entire groups of visitors by their IP address. This is called IP-range blocking. When your monitoring shows attacks coming from a specific set of addresses (like all requests from 45.33.x.x), you create a firewall rule to deny the whole range — blocking the entire crowd of attackers before they can get inside!",
        "reveal": "The two Red Hat IP addresses to block are: 45.33.12.101 (falls in the 45.33.x.x attack range!) and 45.33.198.56 (also in the blocked range — same hacker group!). The other two — 192.168.1.45 (local office network) and 8.8.8.8 (Google's DNS server) — are completely legitimate and safe to allow through.",
        "correctAnswer": "Block: 45.33.12.101 and 45.33.198.56 — both are in the blocked 45.33.x.x attack range",
        "questionText": "Bouncer Eye-Spy! Your firewall alert says: BLOCK ALL connections from IP range 45.33.x.x — these are known attackers wearing 'Red Hats'. A crowd of connection requests is at the door. Click ALL the Red Hat IPs that should be blocked!",
        "emailParts": [
            {"id": "p1", "text": "Connection from: 192.168.1.45 — Office employee laptop on local network", "isFlag": False},
            {"id": "p2", "text": "Connection from: 45.33.12.101 — Unknown external request (in blocked range!)", "isFlag": True},
            {"id": "p3", "text": "Connection from: 8.8.8.8 — Google DNS server (legitimate internet infrastructure)", "isFlag": False},
            {"id": "p4", "text": "Connection from: 45.33.198.56 — Unknown external request (same blocked range!)", "isFlag": True}
        ],
        "correctFlags": ["p2", "p4"]
    },

    # Q16 — decision_simulator (Laser Grid #2: A device tries to skip the firewall)
    # Second format use — Laser Grid themed but different concept (bypassing)
    {
        "local_id": 16, "format": "decision_simulator", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Preventing Firewall Bypass Attempts",
        "hint": "Any device that bypasses or goes around a firewall creates a DATA LEAK gap in the entire network's protection. A firewall only works if EVERYTHING must pass through it!",
        "explain": "A firewall is only effective when all network traffic passes through it — no exceptions. If even one device connects directly to the internet without going through the firewall (like using a phone's 4G data to hotspot a laptop), it creates a gap — a 'Data Leak' — that can be exploited. Every device must use the firewall!",
        "reveal": "The correct response is to report it to IT and reconnect through the firewall-protected network! A personal 4G hotspot bypasses the corporate firewall completely — all traffic to and from that device is now unprotected. This is a serious security violation. The employee probably did not realise the danger, but IT must enforce the policy.",
        "questionText": "Laser Loop Gap! You notice a colleague has connected their work laptop to their personal phone's 4G hotspot instead of the office firewall-protected network. Data could be leaking through this gap! What is the right response?",
        "options": [
            "Say nothing — it is their own phone and their own choice how they connect",
            "Report it to IT and ask the colleague to reconnect through the company's firewall-protected Wi-Fi",
            "Join the same 4G hotspot yourself — if it works for them it must be safe"
        ],
        "correctAnswer": "Report it to IT and ask the colleague to reconnect through the company's firewall-protected Wi-Fi"
    },

    # Q17 — traffic_triage (Pressure Valve #2: Email & web traffic — work vs non-work)
    # Second use of traffic_triage with different scenario (content-based filtering)
    {
        "local_id": 17, "format": "traffic_triage", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Content Filtering at the Firewall",
        "hint": "Content filtering allows work sites and blocks distracting or dangerous categories. Gambling, known malware sites, and streaming (if your policy bans it) should be blocked. Easy!",
        "explain": "Some firewalls include Content Filtering — they block categories of websites rather than just specific IPs. For example, a school or company might block gambling sites, adult content, and known malware distribution sites. This keeps the network both safe AND focused on legitimate activity!",
        "reveal": "ALLOW: github.com (legitimate developer work tool) and slack.com (company communication platform). BLOCK: casino-royale.xyz (gambling site — should never be on a work network!) and malware-downloads.ru (a known malware distribution server — absolutely must be blocked!). Content filtering keeps work networks clean and safe.",
        "correctAnswer": "ALLOW: github.com, slack.com — BLOCK: casino-royale.xyz (gambling), malware-downloads.ru",
        "questionText": "Content Filter Control! Your company firewall has content filtering rules. Sort each web request — should the firewall ALLOW it through or BLOCK it as outside policy?",
        "files": [
            {"id": "f1", "icon": "💻", "name": "github.com — Developer accessing company code repository", "isMalware": False},
            {"id": "f2", "icon": "🎰", "name": "casino-royale.xyz — Employee trying to access a gambling website at work", "isMalware": True},
            {"id": "f3", "icon": "💬", "name": "slack.com — Team using the company's official messaging app", "isMalware": False},
            {"id": "f4", "icon": "💀", "name": "malware-downloads.ru — Known malware distribution server flagged by security databases", "isMalware": True}
        ]
    },

    # Q18 — spot_the_difference / spot_fake (Shadow Filter #2: Compare two firewall rule sets)
    # Second use of spot_fake — find the weaker/worse firewall policy
    {
        "local_id": 18, "format": "spot_fake", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Comparing Firewall Rule Strength",
        "hint": "Which ruleset allows the LEAST amount of unnecessary traffic? A good firewall blocks everything by default and only allows what is specifically needed — not the other way around!",
        "explain": "There are two opposite styles of firewall configuration: 'Deny All by Default' (start with everything blocked, only allow what you need — GOOD!) and 'Allow All by Default' (start with everything open, block what you know is bad — DANGEROUS!). 'Deny All by Default' is always the safer and stronger approach — it minimises the attack surface!",
        "reveal": "NETWORK B's Policy is the safer one — 'Deny all traffic by default; only allow explicitly approved services.' This is the gold standard in firewall security! Network A's 'Allow all traffic by default' policy means everything is allowed unless someone specifically blocks it — hackers love networks set up this way. Always start with DENY and only open what you need!",
        "questionText": "Shadow Filter Showdown! Two office networks have different firewall policies. Which firewall policy is SAFER and should you use as your model?",
        "options": [
            "Network A Policy: Allow all traffic by default — only block known bad IP addresses as we discover them",
            "Network B Policy: Deny all traffic by default — only allow traffic from explicitly approved services and IPs",
            "Network C Policy: No firewall rules at all — let employees browse freely and trust them to be responsible"
        ],
        "correctAnswer": "Network B Policy: Deny all traffic by default — only allow traffic from explicitly approved services and IPs"
    },

    # Q19 — select_all (Circuit Repair #2: Which actions repair a broken firewall?)
    # Second use of select_all — different scenario: what to do after a firewall breach
    {
        "local_id": 19, "format": "select_all", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Responding to a Firewall Breach",
        "hint": "When a firewall has been breached, you need to CONTAIN, INVESTIGATE, and REPAIR — in that order. Select all the actions that contribute to proper recovery!",
        "explain": "When a hacker gets through your firewall, the incident does not end there — it is just beginning. Security teams must respond methodically: isolate the breach, analyse how it happened, patch the gap, and reset compromised credentials. Doing all these steps ensures the attacker cannot use the same route again!",
        "reveal": "The correct repair actions: Temporarily isolate the affected network segment (stop further damage), Review firewall logs to find which rule was exploited (understand the entry point), Patch or update the firewall to fix the gap (close the hole), and Reset all admin account passwords (the attacker may have stolen credentials). Simply rebooting alone wastes precious time and fails to address the root cause!",
        "correctAnswer": "Isolate network, review log, patch firewall, reset passwords — rebooting alone does not fix anything",
        "questionText": "Circuit Repair Emergency! A hacker has breached your company firewall and gained access to the network. Select ALL the correct actions your team should take to repair the damage and stop it happening again:",
        "options": [
            "Immediately reboot the firewall server — this will clear the hacker from the system",
            "Temporarily isolate the affected part of the network to prevent further spread",
            "Review firewall logs to identify exactly which rule or port the hacker exploited",
            "Patch or update the firewall configuration to close the gap that was exploited",
            "Reset all admin and user account passwords in case credentials were stolen",
            "Delete all firewall rules and start fresh — easier than finding the specific problem"
        ],
        "correctFlags": [
            "Temporarily isolate the affected part of the network to prevent further spread",
            "Review firewall logs to identify exactly which rule or port the hacker exploited",
            "Patch or update the firewall configuration to close the gap that was exploited",
            "Reset all admin and user account passwords in case credentials were stolen"
        ]
    },

    # Q20 — the_imposter (Ghost Hunt #2: Find the suspicious admin action in logs)
    # Second use of the_imposter — different context: find malicious admin behaviour
    {
        "local_id": 20, "format": "the_imposter", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Reading Firewall Logs for Suspicious Activity",
        "hint": "Normal admin actions are routine and expected — firmware updates, rule reviews, traffic monitoring. Which action is unusual, unexpected, or would open a dangerous hole in the firewall?",
        "explain": "Firewall logs record every action taken on the system — including by administrators. When attackers gain admin access, they often make stealthy firewall changes: opening ports, deleting rules, or adding backdoor accounts. Reading logs lets security professionals spot these ghost actions and respond quickly!",
        "reveal": "Admin-Ghost is the suspicious one! 'Disabled all inbound firewall rules and set all ports to OPEN' at 3:47 AM is an absolutely catastrophic action — it removes all protection from the network in the middle of the night. No legitimate admin would do this without emergency authorisation. This signature shows an attacker with stolen admin credentials! Sarah and Michael performed routine, legitimately expected admin tasks.",
        "questionText": "Log File Detective! The firewall admin log shows three recent actions. One was made by a Ghost (an attacker using stolen admin credentials) to sabotage the firewall. Find the imposter action!",
        "messages": [
            {"sender": "Admin-Sarah", "text": "Updated firewall firmware to latest version v12.3 — completed at 9:00 AM during scheduled maintenance window", "isPhish": False},
            {"sender": "Admin-Ghost", "text": "Disabled all inbound firewall rules and set all ports to OPEN — action taken at 3:47 AM, no maintenance scheduled", "isPhish": True},
            {"sender": "Admin-Michael", "text": "Reviewed and archived last month's traffic logs — completed at 2:00 PM during normal business hours", "isPhish": False}
        ],
        "options": ["Admin-Sarah", "Admin-Ghost", "Admin-Michael"],
        "correctAnswer": "Admin-Ghost"
    },

    # Q21 — scenario_mcq (Signal Jammer #2: Detect what type of attack is happening)
    # Second use of scenario_mcq with a different firewall scenario
    {
        "local_id": 21, "format": "scenario_mcq", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Identifying a DDoS Attack",
        "hint": "When the attack comes from thousands of different IPs all at once, all hitting the same target, it is NOT a single hacker — it is a coordinated flood. What is the name for this?",
        "explain": "A DDoS (Distributed Denial-of-Service) attack is like thousands of people all trying to walk through a single door at once — the door gets jammed and nobody legitimate can get through. Attackers use networks of compromised computers (called botnets) to flood a target simultaneously. Firewalls can detect the pattern and block the flood using rate-limiting rules!",
        "reveal": "This is a DDoS (Distributed Denial-of-Service) attack! Over 50,000 simultaneous connection requests from thousands of different IPs all hitting your server at once is a textbook DDoS flood. A single hacker tries a few ports. A virus spreads through files. A DDoS floods with traffic from everywhere at once. Firewalls fight this with rate-limiting rules that throttle how many requests one IP can make per second.",
        "questionText": "Signal Detected! Your firewall alarm is blaring: 50,000+ simultaneous connection requests from 10,000+ different IP addresses are all flooding your web server RIGHT NOW! The server is grinding to a halt. What type of attack is this?",
        "options": [
            "A single hacker using one computer to try to guess the admin password",
            "A DDoS (Distributed Denial-of-Service) attack — thousands of devices flooding your server to overwhelm it",
            "A computer virus spreading itself through email attachments to your employees",
            "A phishing attack using fake emails to steal employee login credentials"
        ],
        "correctAnswer": "A DDoS (Distributed Denial-of-Service) attack — thousands of devices flooding your server to overwhelm it"
    },

    # Q22 — branching_narratives (VPN Tunnel #2: Choose correct remote work practice)
    # Second use of branching_narratives, different VPN/remote work scenario
    {
        "local_id": 22, "format": "branching_narratives", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Safe Remote Working with a Firewall and VPN",
        "hint": "Public Wi-Fi hotspots (cafes, airports) have NO protection. Anyone on the same network can potentially intercept your data. What tool creates a safe private tunnel even on public Wi-Fi?",
        "explain": "When you work in a coffee shop or airport on public Wi-Fi, your data travels through a network where strangers could be listening. Connecting to your company's VPN FIRST creates an encrypted private tunnel that protects all your data — even on completely untrusted public networks. This is why most companies require VPN for all remote work!",
        "reveal": "Always connect the company VPN first, then access work systems! This is the golden rule of remote working. Without the VPN, all your work data travels in the open on the public Wi-Fi — anyone on that network with basic tools can intercept it. Incognito mode only hides browsing history on your browser — it does not encrypt your network traffic at all!",
        "questionText": "Remote Work Tunnel! You are working from a coffee shop with public Wi-Fi and need to access confidential company files on the company server. What should you do FIRST?",
        "options": [
            "Just open your browser in Incognito Mode — this keeps your browsing private and secure",
            "Connect to the company VPN first, then access all company systems through the encrypted tunnel",
            "Connect directly to the company server without a VPN — HTTPS should be enough for basic security"
        ],
        "correctAnswer": "Connect to the company VPN first, then access all company systems through the encrypted tunnel"
    },

    # Q23 — scavenger_hunt (Bouncer Eye-Spy #2: Find ALL firewall misconfiguration risks)
    # Second use of scavenger_hunt — find all problems in a firewall config screen
    {
        "local_id": 23, "format": "scavenger_hunt", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Spotting Firewall Misconfigurations",
        "hint": "Well-configured firewalls block dangerous ports, limit access to trusted IPs, and enable logging. Any setting that says 'ANY' IP or 'ALL ports open' is a misconfiguration waiting to be exploited!",
        "explain": "Firewall misconfiguration is the number one cause of avoidable security breaches. Real security auditors check firewall rule lists looking for exactly these problems: open ports that should be closed, rules that allow traffic from any IP, and logging that has been accidentally turned off. Finding these misconfigurations is like being a Bouncer spotting fake IDs at a door!",
        "reveal": "The three misconfigurations: Port 23 (Telnet) left OPEN — Telnet is ancient and transmits passwords in plain text, it must always be blocked! 'Allow SSH from ANY IP' — SSH should only be allowed from specific trusted admin IPs, not the whole internet! 'Firewall logging DISABLED' — without logs you are flying blind and cannot detect or investigate attacks. The HTTPS rule and the updated firmware are both correctly configured.",
        "correctAnswer": "Click: Port 23 open, SSH from ANY IP, and Logging disabled — three dangerous misconfigs!",
        "questionText": "Firewall Audit! You are reviewing the firewall configuration screen. Some settings are fine, but some are dangerously misconfigured. Find and click ALL the misconfigured settings that need immediate fixing by the Bouncer!",
        "objects": [
            {"id": "o1", "icon": "🔒", "label": "Port 443 (HTTPS): OPEN for all verified web traffic — correct configuration", "isRedFlag": False, "top": "10%", "left": "8%"},
            {"id": "o2", "icon": "💀", "label": "Port 23 (Telnet): OPEN — Telnet is insecure and should always be closed!", "isRedFlag": True, "top": "10%", "left": "55%"},
            {"id": "o3", "icon": "💀", "label": "SSH (Port 22): ALLOW from ANY IP address — admin access is open to the whole world!", "isRedFlag": True, "top": "48%", "left": "8%"},
            {"id": "o4", "icon": "💀", "label": "Firewall Logging: DISABLED — no record of traffic means attacks go completely undetected!", "isRedFlag": True, "top": "48%", "left": "55%"},
            {"id": "o5", "icon": "✅", "label": "Firmware Version: Up to date — firewall is running the latest security patches", "isRedFlag": False, "top": "80%", "left": "30%"}
        ]
    },

    # Q24 — decision_simulator (Shield-Bash #2: Respond to a suspicious firewall alert)
    # Second use of decision_simulator — different firewall emergency scenario
    {
        "local_id": 24, "format": "decision_simulator", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Responding to a Firewall Intrusion Alert",
        "hint": "When the firewall detects an intrusion and sends an alert, what should you NOT do? You should isolate the threat, investigate, not just ignore or permanently disable the security tool!",
        "explain": "Firewall alerts are like a fire alarm — when one goes off, you investigate immediately rather than ignoring it or simply turning off the alarm. The correct response to a firewall intrusion alert is to check the logs, isolate the suspicious connection, and escalate to the IT security team. Never disable the firewall as a response to an alert — that leaves you completely unprotected!",
        "reveal": "The correct Shield-Bash response is to immediately check the firewall logs, block the specific suspicious connection, and report to the IT security team! Ignoring the alert means the attack continues. Disabling the whole firewall to 'remove the problem' is exactly what the attacker wants — it removes all remaining defences! Only block the specific threat, not your entire shield.",
        "questionText": "Shield-Bash Emergency! Your firewall sends a CRITICAL ALERT: 'Intrusion detected — suspicious connection from 91.234.0.55 attempting to access database server.' What is the correct Shield-Bash response?",
        "options": [
            "Ignore the alert for now — firewall alerts happen all the time and are usually false alarms",
            "Immediately disable the firewall — it is causing the problem by blocking legitimate traffic",
            "Check the firewall logs, block the specific suspicious IP 91.234.0.55, and report to IT security team immediately"
        ],
        "correctAnswer": "Check the firewall logs, block the specific suspicious IP 91.234.0.55, and report to IT security team immediately"
    },

    # Q25 — sequence_builder (Port Key-Code #2: Order of safely opening a new port)
    # Second use of sequence_builder — how to safely open a new port step by step
    {
        "local_id": 25, "format": "sequence_builder", "difficulty": "beginner",
        "gameName": "firewall", "game_key": "firewall", "level_name": "beginner",
        "concept": "Safely Adding a New Firewall Rule",
        "hint": "You cannot test before you apply. You must document before you finish. And you should always get approval before making permanent changes to a security system. What is the safest logical order?",
        "explain": "Opening a new port in a firewall is a sensitive operation — done wrong, it creates a security hole. Security teams follow a careful process: get approval first, understand exactly what traffic needs to pass through, write the most specific possible rule (not 'allow all'!), test it with safe traffic, and document the change so the whole team knows what was done and why.",
        "reveal": "Correct safe order: 1) Get management approval (security changes need authorisation!), 2) Write the most specific rule possible (only allow the exact port and IP range needed), 3) Apply the rule to the firewall in a test/staging environment, 4) Test with safe controlled traffic to confirm it works correctly, 5) Document the change in the team's security log. This methodical process prevents accidental security holes!",
        "questionText": "Port Key-Code Sequence! Your team needs to open Port 8080 for a new web application. Arrange the 5 steps in the correct ORDER to do this safely without creating a security risk!",
        "steps": [
            {"id": "s1", "text": "Get management and IT security team approval for the new firewall rule", "correctOrder": 0},
            {"id": "s2", "text": "Write the most specific rule possible: only allow the exact IPs and ports needed for the application", "correctOrder": 1},
            {"id": "s3", "text": "Apply the rule to the firewall in a test environment first", "correctOrder": 2},
            {"id": "s4", "text": "Test the new rule with controlled safe traffic to confirm it works as expected", "correctOrder": 3},
            {"id": "s5", "text": "Document the new rule in the team's firewall change log with date, reason, and responsible person", "correctOrder": 4}
        ]
    }
]

result = col.insert_many(questions)
count = col.count_documents({'game_key': 'firewall', 'level_name': 'beginner'})
print("Inserted: " + str(len(result.inserted_ids)) + " firewall beginner questions")
print("Total firewall beginner questions in DB: " + str(count))
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
if all_ok:
    print("\nAll good -- no consecutive duplicate formats!")
else:
    print("\nWARNING: Some consecutive duplicates found above!")

client.close()
