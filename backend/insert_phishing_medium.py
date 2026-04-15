from dotenv import load_dotenv
import os
load_dotenv()
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGO_URI'))
col = client['cyberduo']['questions']

col.delete_many({'game_key': 'phishing', 'level_name': 'medium'})

questions = [

    # Q1 — digital_whodunnit (Header Investigator: Return-Path vs From)
    {
        "local_id": 1, "format": "digital_whodunnit", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "Email Header Spoofing — SPF and DKIM Analysis",
        "hint": "A legitimate email passes BOTH SPF and DKIM. A spoofed email almost always fails at least one — the sending server is not authorised or the domain signature cannot be verified. Which row shows FAIL results?",
        "explain": "SPF (Sender Policy Framework) validates that the sending mail server is authorised by the domain owner. DKIM (DomainKeys Identified Mail) verifies the email content was not altered in transit. When both fail — or the Return-Path domain differs from the From address — the email is definitively spoofed. Real phishing detectives check these header values before any other indicator!",
        "reveal": "The spoofed email is from 'noreply@paypal-security.com'! SPF FAIL (the sending server is not authorised by paypal.com) and DKIM FAIL (the domain signature cannot be verified) are definitive proof. Attackers register lookalike domains like 'paypal-security.com' — the word 'paypal' appears but the actual root domain is different. Always check both SPF and DKIM, not just the visible From address.",
        "questionText": "Header Investigator! Three emails arrived. Study the SPF and DKIM authentication results for each sender address. Which email is SPOOFED?",
        "emails": [
            {"id": "e1", "from": "support@amazon.com", "spf": "PASS", "dkim": "PASS"},
            {"id": "e2", "from": "noreply@paypal-security.com", "spf": "FAIL", "dkim": "FAIL"},
            {"id": "e3", "from": "newsletter@spotify.com", "spf": "PASS", "dkim": "PASS"}
        ],
        "options": ["support@amazon.com", "noreply@paypal-security.com", "newsletter@spotify.com"],
        "correctAnswer": "noreply@paypal-security.com"
    },

    # Q2 — spot_fake (Spoof-Check Slider: Microsoft real vs fake domain)
    {
        "local_id": 2, "format": "spot_fake", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "Look-Alike Domain Spoofing — Sliding Transparency Filter",
        "hint": "Microsoft's official authentication domain is always microsoft.com or login.microsoftonline.com. Any .net, .org, or hyphenated variation is a registered fake — even if 'microsoft' appears in the domain name!",
        "explain": "Homograph and lookalike domain attacks rely on users scanning quickly and seeing the brand name without reading the full domain. 'microsoft-security.net' looks professional because it contains the real word 'microsoft' — but the .net TLD and the appended '-security' reveal it is a registered attacker domain. Always read the ROOT domain (right before .com/.net/.org) rather than just scanning for brand names.",
        "reveal": "The FAKE is 'microsoft-security.net'. Microsoft's sign-in is ONLY at login.microsoftonline.com or microsoft.com — never a .net domain. The real login URL starts with 'login.microsoftonline.com' — the 'microsoft' part is in the domain, not a lookalike subword. Attackers register domains like microsoft-security.net, microsoft-account-verify.net, and microsoftonline-support.com to host perfect copies of real Microsoft login pages.",
        "questionText": "Spoof-Check Slider! An email says 'Verify your Microsoft account immediately'. Slide the Transparency Filter over each address below. Which one is the DANGEROUS FAKE?",
        "options": [
            "login.microsoftonline.com — The legitimate Microsoft Office 365 sign-in URL",
            "microsoft-security.net — Looks official but is NOT on Microsoft's real domain",
            "microsoft.com/en-us/security — Microsoft's official security information page"
        ],
        "correctAnswer": "microsoft-security.net — Looks official but is NOT on Microsoft's real domain"
    },

    # Q3 — quishing_drill (HR Policy Fake QR — Quishing)
    {
        "local_id": 3, "format": "quishing_drill", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "QR Code Phishing (Quishing) — Fake Internal Document",
        "hint": "Your company's HR portal will always be on your company's own domain. Any QR code pointing to a .xyz, .info, .co, or other external domain is quishing — QR phishing targeting employees who trust official-looking printed documents!",
        "explain": "Quishing (QR phishing) hides malicious URLs inside QR codes embedded in documents, emails, or physical materials. Attackers print posters or circulate PDFs that look like internal HR documents — employees scan them out of compliance habit. The attack is effective because most mobile QR scanners display the URL only briefly. Always check the FULL decoded URL before tapping to open.",
        "reveal": "PHISHING! The QR code goes to 'hr-portal-login.xyz' — a completely external domain. Your company's real HR portal would be on a company-owned domain (e.g., hr.yourcompany.com). The .xyz TLD combined with 'hr-portal-login' is a classic quishing domain setup designed to harvest employee credentials from people who assume they are accessing a legitimate company system. Report the document to IT Security immediately!",
        "questionText": "Quishing Scan! A printed 'Company HR Policy Update Q2 2025' in the break room has a QR code: 'Scan here to log in and acknowledge receipt.' Click SCAN to decode the QR code — Safe or Phishing?",
        "qrObject": "📋 Printed A4: COMPANY HR POLICY UPDATE — Q2 2025\nAll employees must acknowledge receipt by scanning the QR code and logging into the policy portal.",
        "decodedURL": "https://hr-portal-login.xyz/company-authenticate?redirect=policy2025",
        "correctAnswer": "Phishing"
    },

    # Q4 — the_imposter (Spear-Phish Profile Match: personalised email using LinkedIn data)
    {
        "local_id": 4, "format": "the_imposter", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "Spear Phishing — Targeted Attack Using Public Social Media Data",
        "hint": "A spear-phish uses specific personal details scraped from your LinkedIn or social media — details a generic mass phishing email would NOT know. Which message references something very specific and personal about YOU?",
        "explain": "Spear phishing is targeted: attackers research victims via LinkedIn, Facebook, and Twitter before crafting personalised emails. Details like your recent promotion, employer name, department, or colleagues' names make the fake email seem credible. Generic phishing says 'Dear Customer' — spear phishing says 'Congratulations on your promotion to Senior Manager, Finance Department!' The personalisation lowers your guard.",
        "reveal": "The spear-phish is from 'IT-Support@yourcompany-helpdesk.net'! It references your 'recent promotion to Senior Manager in Finance' — details scraped from your public LinkedIn. But the real red flag is the domain: legitimate IT support emails come from @yourcompany.com (your real domain), not @yourcompany-helpdesk.net (a registered lookalike). The personalised detail is the lure; the lookalike domain is the trap.",
        "questionText": "Spear-Phish Radar! Your LinkedIn shows you were recently promoted to Senior Manager, Finance. Three emails just arrived. Which one is a personalised SPEAR PHISH using your public profile data?",
        "messages": [
            {"sender": "hr@yourcompany.com", "text": "Hi team — please review the attached Q2 leave policy. No action required unless the new rules affect your schedule.", "isPhish": False},
            {"sender": "IT-Support@yourcompany-helpdesk.net", "text": "Congratulations on your recent promotion to Senior Manager, Finance! Please verify your updated access permissions by re-entering your credentials at the secure link below to avoid disruption.", "isPhish": True},
            {"sender": "finance-team@yourcompany.com", "text": "Monthly budget tracker for Q2 is attached. Please complete your section by Friday for the CFO's review.", "isPhish": False}
        ],
        "options": ["hr@yourcompany.com", "IT-Support@yourcompany-helpdesk.net", "finance-team@yourcompany.com"],
        "correctAnswer": "IT-Support@yourcompany-helpdesk.net"
    },

    # Q5 — decision_simulator (Fake Login Page: what to do when URL looks wrong)
    {
        "local_id": 5, "format": "decision_simulator", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "Suspicious Login Page — Acting on a Wrong URL",
        "hint": "Your bank's real website is always yourbank.com — nothing added in front or after. If the address bar shows anything different, trust your gut and EXIT before entering anything!",
        "explain": "Phishing pages often look pixel-perfect copies of real login pages. The ONLY reliable indicator is the URL in the browser address bar. If the domain is not exactly the bank's official root domain, the page is fake. Entering credentials even once is enough for the attacker to take over your account — because the fake page captures your input and relays it immediately.",
        "reveal": "Close the tab immediately and go directly to your bank by typing the URL yourself! You spotted the wrong URL — that is the key skill. Calling the bank to report it adds an extra protective step so the fake site can be reported and taken down. Never enter any detail on a page where the URL does not exactly match the real company domain.",
        "questionText": "Suspicious Login Page! You click a link in an email and a bank login page appears. It looks exactly like your bank — logo, colours, everything. But the address bar shows: 'lloyds-secure-login.net' instead of 'lloydsbank.co.uk'. What do you do?",
        "options": [
            "Log in anyway — the page looks completely genuine and identical to the real one",
            "Close the tab immediately, go directly to lloydsbank.co.uk by typing it yourself, and call the bank to report the fake page",
            "Try entering just your username first — if the page rejects invalid names, it must be the real bank"
        ],
        "correctAnswer": "Close the tab immediately, go directly to lloydsbank.co.uk by typing it yourself, and call the bank to report the fake page"
    },

    # Q6 — file_triage (Look-Alike Domain Sort #1: Safe vs Evil)
    {
        "local_id": 6, "format": "file_triage", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "Homograph Domain Classification — Safe vs Evil Bins",
        "hint": "Look at EVERY character individually. A capital letter 'I' looks identical to a lowercase 'L' in most fonts. A zero '0' looks like the letter 'o'. Additions like '-login', '-secure', or '-id' are also danger signals for legitimate brand domains.",
        "explain": "Homograph attacks use character substitutions invisible to normal reading speed. 'paypaI.com' (capital I) and 'paypal.com' (lowercase L) look identical in most font renderings — but they are completely different domains. Developing the habit of reading URL characters individually — especially in financial or authentication contexts — is essential for medium-level phishing detection.",
        "reveal": "SAFE: paypal.com (official) and apple.com (official). EVIL: paypaI.com (capital letter 'I' replacing 'l' in paypal — a completely different registered domain!) and apple-id-1ogin.com (uses numeric '1' and '0' instead of 'l' and 'o' — unmistakable character substitutions). Both evil domains are registered by phishers and host perfect visual copies of the real login pages.",
        "correctAnswer": "SAFE: paypal.com, apple.com — EVIL: paypaI.com (capital I), apple-id-1ogin.com (1 and 0 substitutions)",
        "questionText": "Look-Alike Domain Sort! Drag each domain into the SAFE bin or EVIL bin. Examine EVERY character — some fakes are almost invisible at normal reading speed!",
        "files": [
            {"id": "f1", "icon": "💳", "name": "paypal.com — Official PayPal payment platform", "isMalware": False},
            {"id": "f2", "icon": "💀", "name": "paypaI.com — Uses capital letter I (not lowercase L) — different domain!", "isMalware": True},
            {"id": "f3", "icon": "🍎", "name": "apple.com — Official Apple website", "isMalware": False},
            {"id": "f4", "icon": "💀", "name": "apple-id-1ogin.com — Uses '1' and '0' substitutions instead of 'l' and 'o'", "isMalware": True}
        ]
    },

    # Q7 — click_flags (Tone Analyzer: highlight urgency language in phishing email)
    {
        "local_id": 7, "format": "click_flags", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "Identifying False Urgency Language in Phishing Emails",
        "hint": "Urgency language forces panicked, unthinking responses. Words like 'IMMEDIATE', 'UNAUTHORIZED', and 'PERMANENTLY SUSPENDED in 24 hours' together form the classic phishing pressure trifecta — click all three!",
        "explain": "Phishing emails use high-pressure language to bypass your rational thinking. 'False urgency' phrases — countdown timers, 'final' warnings, 'unauthorized' activity alerts — remove thinking time and push you toward the link. Real banks and companies send routine notifications, not EMERGENCY COUNTDOWN WARNINGS. Any email that triggers emotional panic should be forensically examined before any action.",
        "reveal": "Three urgency red flags: 'IMMEDIATE action required' (pressure command), 'UNAUTHORIZED login detected from Russia' (fear-inducing false alarm), and 'PERMANENTLY SUSPENDED in 24 hours' (countdown threat). Together these three form the complete urgency/fear/deadline trifecta used by professional phishing campaigns. The sender domain and greeting are also suspicious but are not urgency language specifically.",
        "correctAnswer": "Click: IMMEDIATE action required, UNAUTHORIZED login, PERMANENTLY SUSPENDED in 24 hours",
        "questionText": "Tone Analyzer! Read this email excerpt and click ALL the phrases that create FALSE URGENCY — the psychological pressure tactics designed to make you panic and click without thinking:",
        "emailParts": [
            {"id": "p1", "text": "From: security-alerts@yourbank-secure.net", "isFlag": False},
            {"id": "p2", "text": "Subject: IMMEDIATE action required — Your account security", "isFlag": True},
            {"id": "p3", "text": "Dear Valued Customer,", "isFlag": False},
            {"id": "p4", "text": "We detected UNAUTHORIZED login activity on your account originating from Russia.", "isFlag": True},
            {"id": "p5", "text": "Your account will be PERMANENTLY SUSPENDED in 24 hours unless you verify your identity now.", "isFlag": True}
        ],
        "correctFlags": ["p2", "p4", "p5"]
    },

    # Q8 — scenario_mcq (SSL Inspector: invalid certificate issuer on bank login)
    {
        "local_id": 8, "format": "scenario_mcq", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "SSL Certificate Verification — Checking the Certificate Issuer",
        "hint": "A padlock icon alone does NOT prove a site is safe — phishing sites get HTTPS certificates too! Click the padlock and check WHO the certificate was issued TO. It must match the company's exact registered legal name.",
        "explain": "HTTPS only means traffic is encrypted in transit — it says nothing about whether the server is legitimate. Attackers obtain free SSL certificates (via Let's Encrypt) to display a padlock on phishing pages. The critical verification is clicking the padlock and checking the certificate Subject: it should be the company's registered legal name. A certificate issued to 'Unknown_Entity_Ltd' on a bank login page is a definitive phishing indicator.",
        "reveal": "Hit the EMERGENCY EXIT! The certificate was issued to 'Unknown_Entity_Ltd' — not to your bank's registered company name. Legitimate banks maintain CA-issued certificates showing their exact registered legal name in the Subject field (e.g., 'Barclays Bank UK PLC' or 'Lloyds Bank plc'). A certificate issued to an unrelated entity confirms that someone else registered this domain and obtained a certificate — characteristics of a phishing site.",
        "questionText": "SSL Inspector! You are on what looks like your bank's login page. There is a padlock in the address bar. You click the padlock and read: 'Certificate issued to: Unknown_Entity_Ltd'. What is the correct action?",
        "options": [
            "Proceed and log in — the padlock means the connection is fully encrypted and therefore secure",
            "Hit the EMERGENCY EXIT — a certificate issued to an unrecognised entity confirms this is a phishing page",
            "Refresh the page and try again — the certificate display is probably a temporary browser rendering error",
            "Enter only your username first as a test — if it fails, then you know the site is fake"
        ],
        "correctAnswer": "Hit the EMERGENCY EXIT — a certificate issued to an unrecognised entity confirms this is a phishing page"
    },

    # Q9 — link_inspector (Short-Link Expander: bit.ly hiding malicious destination)
    {
        "local_id": 9, "format": "link_inspector", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "URL Shortener Expansion — Revealing Hidden Phishing Destinations",
        "hint": "Short links (bit.ly, t.co, tinyurl) completely hide the real destination. In a suspicious email context, ALWAYS expand before clicking. If the real URL domain is not the official company domain — it is phishing!",
        "explain": "URL shorteners legitimately compress long marketing URLs — but attackers abuse them specifically to hide malicious destinations from email security scanners. bit.ly links can redirect to any URL without exposing it in the short link. In a phishing email, the expanded destination reveals the truth: real Netflix billing pages are ONLY on netflix.com. Any other domain is a phishing clone.",
        "reveal": "PHISHING! The short link hides 'www.netflix-billing-update.xyz/pay-now' — not netflix.com. Netflix billing pages exist ONLY on netflix.com (or country equivalents). The .xyz domain with 'netflix-billing' in the path is a fake credential and payment card harvesting page. Short links are used precisely because the malicious URL itself would be blocked by email security tools if sent without obfuscation.",
        "questionText": "Short-Link Expander! An email from 'Netflix Billing' says: 'Your payment failed. Update your information immediately: bit.ly/nflx-billing-2025'. Hover the link to expand it. Where does it REALLY go?",
        "displayedLink": "bit.ly/nflx-billing-2025 → [Hover to reveal real URL]",
        "actualDestination": "https://www.netflix-billing-update.xyz/pay-now?session=tracked&user=target",
        "correctAnswer": "Phishing"
    },

    # Q10 — branching_narratives (Shared Doc Trap: delete without opening)
    {
        "local_id": 10, "format": "branching_narratives", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "Fake Shared Document Notification — Unexpected File Alert",
        "hint": "The key question is always: did you EXPECT this file? If not, the safest action is to NOT click the link at all — verify with the sender directly using a separate channel like Slack or a phone call.",
        "explain": "Shared document notifications (Google Drive, OneDrive, Dropbox) are spoofed by attackers because employees receive them routinely. The link in the email may go to a fake Google sign-in page that harvests your credentials. Forwarding the email to your manager without verification does NOT protect you — you or your manager could still click the link. The correct action is to verify with Tim DIRECTLY using a separate channel, BEFORE touching the link.",
        "reveal": "Delete without opening and contact Tim directly through a separate channel — like Slack, a phone call, or a new email! This is the complete safe action. Forwarding to your manager sounds helpful but still risks someone clicking the malicious link before Tim confirms. Even if Tim is real, his account may have been compromised and is auto-sharing malware to his contacts. Always direct-verify before clicking unexpected shared files.",
        "questionText": "'Shared Doc' Trap! A notification arrives: 'Tim_from_Finance shared a Google Doc: Q2_Salary_Review_CONFIDENTIAL.pdf — click to view.' You do NOT remember requesting or expecting any file from Tim. What is the SAFEST response?",
        "options": [
            "Click the link — Tim is a real colleague and the file title sounds genuinely work-related",
            "Delete without opening, then message or call Tim directly through a separate channel to confirm he sent it",
            "Forward it to your manager so they can open it — if it's malicious, let IT deal with it"
        ],
        "correctAnswer": "Delete without opening, then message or call Tim directly through a separate channel to confirm he sent it"
    },

    # Q11 — click_flags (Signature Match: find mismatching details vs Company Directory)
    {
        "local_id": 11, "format": "click_flags", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "Email Signature Inconsistency Detection",
        "hint": "Compare every detail in the email signature against the Company Directory entry for the same person. The attacker got the name and title right from LinkedIn — but internal details like phone extension, department name, and reporting line are wrong!",
        "explain": "Impersonators researching a target company via LinkedIn and Companies House get the name, title, and general role right — but they do not have access to the internal company directory. Small but consistent errors appear in internal-facing details: phone extension numbers, exact department sub-names, reporting hierarchy, and physical office location. Cross-referencing email signatures against the directory is a powerful detection technique.",
        "reveal": "Three mismatches: phone extension (4491 in email vs 4419 in directory — transposed digits!), department name ('Group Finance' vs directory's 'Corporate Finance'), and reporting line ('reports to CFO' vs directory's 'reports to Financial Controller'). These three errors together show the sender researched publicly available information but could not access internal directory data — a reliable sign of an impersonation attempt.",
        "correctAnswer": "Click 3 mismatches: phone extension (4491 vs 4419), department (Group vs Corporate Finance), and reporting manager",
        "questionText": "Signature Match! Compare this email signature against the Company Directory for David Chen, Finance. Click ALL the details that DO NOT MATCH the official directory record:",
        "emailParts": [
            {"id": "p1", "text": "David Chen — Finance Manager (Job title: MATCHES directory ✓)", "isFlag": False},
            {"id": "p2", "text": "Phone: +44 20 7946 ext. 4491 (Directory records: ext. 4419 — digits transposed!)", "isFlag": True},
            {"id": "p3", "text": "david.chen@yourcompany.com (Email address: MATCHES directory ✓)", "isFlag": False},
            {"id": "p4", "text": "Department: Group Finance (Directory records: Corporate Finance — wrong sub-name!)", "isFlag": True},
            {"id": "p5", "text": "Reports to: CFO Sarah Williams (Directory records: reports to Financial Controller Mark Brown!)", "isFlag": True}
        ],
        "correctFlags": ["p2", "p4", "p5"]
    },

    # Q12 — decision_simulator (External Tag Spotter: email claims to be internal but has EXTERNAL tag)
    {
        "local_id": 12, "format": "decision_simulator", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "External Email Tag — Detecting Spoofed Internal Sender Addresses",
        "hint": "Corporate email systems tag all externally-originating emails with an [EXTERNAL] banner. If an email claiming to be from your internal IT team carries this tag, it definitively did NOT come from inside your company — it was SPOOFED or sent from outside!",
        "explain": "The [EXTERNAL] banner is added automatically by enterprise email gateways (Microsoft 365, Google Workspace) to all emails arriving from outside the organisation's own email domain. If an email appears to be from IT_Support@yourcompany.com but shows EXTERNAL, the real sending domain is different — the From address was spoofed. IT departments communicate via internal systems, not external email addresses, and never request credentials via email.",
        "reveal": "Click the EXTERNAL tag and report as phishing! The email claims to be from your internal IT support at @yourcompany.com, but the EXTERNAL banner is definitive proof it was sent from outside your company's email domain. This is a spoofed sender address — a classic phishing technique targeting employees who trust messages from their own IT team. Real internal IT teams use ticketing systems, not external emails asking for password re-entry.",
        "questionText": "External Tag Alert! An email claiming to be from 'IT-Support@yourcompany.com' says: 'Re-enter your network credentials via the link below — urgent system migration in progress.' At the TOP is a yellow banner: ⚠️ [EXTERNAL — This email originated outside the organisation]. What do you do?",
        "options": [
            "Click the link — the IT team sometimes sends from external hosting services during major migrations",
            "Click the EXTERNAL tag to confirm the spoofing attempt and report the email as phishing",
            "Reply to the email asking IT to confirm they sent it before you enter any credentials"
        ],
        "correctAnswer": "Click the EXTERNAL tag to confirm the spoofing attempt and report the email as phishing"
    },

    # Q13 — sequence_builder (Redirect Maze: correct steps to handle suspicious redirect)
    {
        "local_id": 13, "format": "sequence_builder", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "Incident Response — Clicked a Suspicious Redirect Link",
        "hint": "When you spot a suspicious redirect chain, speed matters. Disconnect FIRST to stop any active data transmission, then preserve evidence, then report. Never just close the tab and forget about it!",
        "explain": "Legitimate websites use zero or one redirect hop. Phishing chains use multiple hops to: evade URL filtering (initial URL looks clean), track victim data across servers, and pass credentials to a backend collector. Spotting unusual server geographies (blacklisted countries) in the chain lets you abort before the malicious final page loads. Immediate disconnection stops any ongoing data exfiltration.",
        "reveal": "Correct sequence: 1) Notice unexpected redirects (alert signal!), 2) Identify any blacklisted country servers in the chain, 3) Disconnect from the internet immediately — before the final page loads, 4) Preserve evidence: screenshot the URL chain without closing, 5) Report to IT Security with the complete URL chain and timing. This sequence minimises exposure and gives IT the intelligence they need to prevent other employees being targeted.",
        "questionText": "Redirect Maze! You clicked a supplier link and your data packet is visibly travelling through 3 different servers. You notice one server is in a blacklisted country. Arrange these 5 response steps in the CORRECT order:",
        "steps": [
            {"id": "s1", "text": "Notice: the link is routing through multiple unexpected intermediate servers", "correctOrder": 0},
            {"id": "s2", "text": "Identify: note which country servers appear in the chain — flag blacklisted geographies", "correctOrder": 1},
            {"id": "s3", "text": "Disconnect: close the browser or cut internet immediately — before the final page loads", "correctOrder": 2},
            {"id": "s4", "text": "Preserve: screenshot the URL chain for IT Security evidence without reopening the link", "correctOrder": 3},
            {"id": "s5", "text": "Report: send the complete redirectchain URL and screenshots to IT Security for blacklisting", "correctOrder": 4}
        ]
    },

    # Q14 — digital_whodunnit #2 (SPF PASS DKIM FAIL typosquatting)
    {
        "local_id": 14, "format": "digital_whodunnit", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "Advanced Header Analysis — SPF Pass DKIM Fail Pattern",
        "hint": "An email that PASSES SPF but FAILS DKIM is a sophisticated red flag. The attacker has a real mail server for their fake domain (SPF passes) but cannot replicate the real company's private DKIM key (DKIM fails). Also: look very carefully at every character in the From domain!",
        "explain": "SPF passing with DKIM failing is the signature of a typosquatting domain impersonation attack. The attacker registered 'netf1ix.com' (with a '1' replacing 'l'), set up a real mail server for it (so SPF checks pass), but cannot reproduce the real Netflix's DKIM private key. This combination is increasingly common as attackers set up legitimate infrastructure for lookalike domains to bypass simple SPF-only security filters.",
        "reveal": "The spoofed sender is 'billing@netf1ix.com' (with a number '1' replacing the letter 'l'). SPF PASS confirms the attacker's own domain has a proper mail server configured. DKIM FAIL confirms they cannot replicate the real Netflix's cryptographic private key. Visually, 'netf1ix' looks almost identical to 'netflix' in most email clients — this is why header inspection matters more than visual domain checking alone.",
        "questionText": "Header Investigation Round 2! One email is from a typosquatted domain that passes SPF (attacker has their own mail server) but fails DKIM (cannot fake the real company's private signing key). Spot the SPOOFED sender!",
        "emails": [
            {"id": "e1", "from": "security@google.com", "spf": "PASS", "dkim": "PASS"},
            {"id": "e2", "from": "billing@netf1ix.com", "spf": "PASS", "dkim": "FAIL"},
            {"id": "e3", "from": "noreply@github.com", "spf": "PASS", "dkim": "PASS"}
        ],
        "options": ["security@google.com", "billing@netf1ix.com", "noreply@github.com"],
        "correctAnswer": "billing@netf1ix.com"
    },

    # Q15 — quishing_drill #2 (Package Delivery Customs Fee)
    {
        "local_id": 15, "format": "quishing_drill", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "Package Delivery QR Phishing — Fake Customs Fee",
        "hint": "Royal Mail, UPS, FedEx, and DHL NEVER ask you to scan a QR code in an email to pay customs fees. Customs fee notifications arrive by physical card through the post — not email QR codes! Any QR redirecting to a third-party payment domain is phishing.",
        "explain": "Package delivery quishing exploits parcel anticipation — most people are waiting for something. 'Failed delivery' or 'customs fee outstanding' messages trigger immediate action. Real courier customs processes: Royal Mail sends a physical RED card through your letterbox with a reference number. All legitimate tracking and payment happens on the carrier's official domain only. Third-party payment domains in QR codes are 100% phishing setups.",
        "reveal": "PHISHING! The decoded URL 'parcel-customs-payment.co' is not royalmail.com, ups.com, fedex.com, or any legitimate courier domain. Real UK customs fees for Royal Mail are accessed only at royalmail.com — and you receive a physical red card first, not an email with a QR code. This is a fake payment page designed to steal your card details under urgency pressure.",
        "questionText": "Quishing Scan! An email says: 'Your parcel (RW1234567GB) has an outstanding customs fee of £2.99. Scan the QR code to pay and release your delivery.' Click SCAN to decode. Safe or Phishing?",
        "qrObject": "📦 Email from: parcel-services@delivery-notifications.net\nSubject: ACTION REQUIRED: Pay £2.99 to release your parcel from customs",
        "decodedURL": "https://parcel-customs-payment.co/pay?ref=RW1234567GB&fee=2.99&carrier=RM",
        "correctAnswer": "Phishing"
    },

    # Q16 — spot_fake (AI-Generated Bot Text Detection)
    {
        "local_id": 16, "format": "spot_fake", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "AI-Generated Phishing Emails — Detecting Bot Text Patterns",
        "hint": "AI-generated phishing is grammatically flawless — but it reads like a formal legal notice, not a normal office email from a colleague. Look for hyper-formal phrasing, comprehensive reassurances covering every objection, and urgency embedded in polished language.",
        "explain": "Attackers now use AI tools (ChatGPT variants) to generate grammatically perfect phishing emails that bypass old 'broken English' detection filters. AI-generated phishing is typically hyper-formal, uses legalese ('pursuant to', 'in accordance with', 'compliance protocol'), provides extensive reassurances ('fully protected', 'no inconvenience'), and embeds the call-to-action at the end of formally constructed paragraphs. Compare this to real human office emails — which are casual, contextual, and imperfect.",
        "reveal": "Email 2 is AI-generated! Key tells: 'Pursuant to our security compliance protocol' (no real IT colleague writes this), 'in accordance with GDPR data protection requirements' (buzzword-stacking), 'Rest assured your data is fully protected' (over-reassurance — real IT just asks you to do the task). Compare to Email 1 (natural office casual language with a real human slip 'def check') and Email 3 (short, context-free, genuinely casual). AI phishing reads like a legal brief. Real humans write like humans.",
        "questionText": "AI-Text Humanity Test! Run the scanner on these three emails. One was assembled by an AI bot to phish employees — perfectly worded but characteristically non-human. Which one is the AI-GENERATED PHISHING EMAIL?",
        "options": [
            "Email 1: Hey Sarah, can you def check the Q2 numbers before Thursday's meeting? Might be a couple thou off. Cheers — Mike",
            "Email 2: Dear Esteemed Colleague, Pursuant to our security compliance protocol and in accordance with GDPR requirements, we request your immediate action to verify your credentials via the enclosed link. Rest assured your data is fully protected and no inconvenience is intended.",
            "Email 3: Hi all — just confirming the floor 2 printer has been fixed and is back online. IT Team"
        ],
        "correctAnswer": "Email 2: Dear Esteemed Colleague, Pursuant to our security compliance protocol and in accordance with GDPR requirements, we request your immediate action to verify your credentials via the enclosed link. Rest assured your data is fully protected and no inconvenience is intended."
    },

    # Q17 — the_imposter #2 (CEO BEC impersonation)
    {
        "local_id": 17, "format": "the_imposter", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "CEO/Executive Impersonation — Business Email Compromise (BEC)",
        "hint": "Emails from CEOs demanding urgent, secret financial actions are almost always BEC (Business Email Compromise) attacks. Look at the sending domain carefully — even one character difference from your CEO's real email domain identifies the fake!",
        "explain": "Business Email Compromise impersonates executives (CEO, CFO) to instruct employees to approve unusual financial actions. Red flags: an unusual financial request (wire transfer, gift cards), demands for confidentiality (prevents normal verification), extreme urgency (no time to verify), and an email address that is almost-but-not-exactly your company's real domain. Any financial request from an executive should be verified by a direct phone call to their known number.",
        "reveal": "The BEC imposter is from 'james_morgan@yourcompany-group.net'! Real emails from your CEO come from @yourcompany.com — not '@yourcompany-group.net' (a registered lookalike domain). The £85,000 wire transfer + 2-hour deadline + 'do not discuss with anyone' + 'I cannot take calls' formula is the textbook BEC attack pattern used globally to steal billions per year. Call the CEO directly on their saved number to verify any wire transfer request.",
        "questionText": "BEC Alert! Three emails from 'James' your CEO arrived. One is a BEC impersonation from a lookalike domain. Find the IMPOSTER!",
        "messages": [
            {"sender": "james.morgan@yourcompany.com", "text": "Team — please review the attached Board Minutes from yesterday's session. Action items are highlighted in yellow. Thanks, JM", "isPhish": False},
            {"sender": "james_morgan@yourcompany-group.net", "text": "I need you to process a CONFIDENTIAL wire transfer of £85,000 to a new supplier within 2 hours. Do not discuss with colleagues — I am in a board meeting and cannot take calls. Process immediately.", "isPhish": True},
            {"sender": "james.morgan@yourcompany.com", "text": "Q2 all-hands meeting Thursday at 10AM. Please check the agenda I shared earlier and come ready with department updates!", "isPhish": False}
        ],
        "options": ["james.morgan@yourcompany.com (Board Minutes)", "james_morgan@yourcompany-group.net (Wire Transfer)", "james.morgan@yourcompany.com (All-Hands)"],
        "correctAnswer": "james_morgan@yourcompany-group.net (Wire Transfer)"
    },

    # Q18 — link_inspector #2 (Subdomain manipulation: paypal.com.secure-verification.com)
    {
        "local_id": 18, "format": "link_inspector", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "Subdomain Manipulation — Reading URLs Right-to-Left",
        "hint": "Read URLs from RIGHT to LEFT: start with the TLD (.com, .net), then the ROOT domain (the word before the TLD), then the subdomain path. Attackers put the real brand name as a subdomain — but the ROOT domain is theirs, not the brand's!",
        "explain": "Subdomain manipulation is one of the most effective URL spoofing techniques because the real brand name DOES appear in the URL. 'paypal.com.secure-verification.com' — users see 'paypal.com' and stop reading. But reading right to left: .com TLD → 'secure-verification' ROOT domain → 'paypal.com' is just a subdomain label. The actual site controlled is 'secure-verification.com', which is NOT paypal.com.",
        "reveal": "PHISHING! Reading right to left: the root domain is 'secure-verification.com' — 'paypal.com' is merely a subdomain label. The real PayPal URL structure is 'paypal.com/something' — 'paypal.com' is always the root, never a subdomain of something else. This technique fools many experienced users on first glance. Train yourself to always locate the root domain by reading from the right side of the URL.",
        "questionText": "Spoof-Check! A PayPal email asks you to 'verify your account'. Hover the button to see the full URL path. Is this the real PayPal or a spoofed subdomain trap?",
        "displayedLink": "Verify Your PayPal Account → [Hover to inspect full URL]",
        "actualDestination": "https://paypal.com.secure-verification.com/login?session=tracking_ref_009",
        "correctAnswer": "Phishing"
    },

    # Q19 — select_all (Tone Analyzer #2: all HMRC fake email urgency/authority phrases)
    {
        "local_id": 19, "format": "select_all", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "Recognising ALL Urgency and Authority Manipulation Tactics",
        "hint": "Look for phrases that create time pressure, invoke institutional authority to suppress questioning, generate fear of severe consequences, OR isolate you from verification channels. Select EVERY phrase that manipulates rather than informs!",
        "explain": "Sophisticated phishing uses TWO psychological levers simultaneously: URGENCY (removes thinking time) + AUTHORITY (impersonating HMRC, courts, FBI inhibits scepticism). Real HMRC communications: arrive by post with a specific tax reference number, do not involve dramatic deadlines, and NEVER prohibit you from contacting your bank. The 'do not contact your bank' instruction is especially dangerous — it is an isolation tactic cutting off your best verification route.",
        "reveal": "All five are manipulation tactics: 'FINAL WARNING' (fake countdown urgency), 'HMRC Legal Enforcement Division' (false authority claim — this division does not exist with this title), 'immediate action or face legal prosecution' (fear + urgency combined), 'Do NOT contact your bank' (isolation tactic — the most dangerous instruction in any phishing email!), and 'Deadline: Tomorrow 09:00 GMT' (fake artificial deadline). Real HMRC sends letters with specific reference codes — never email ultimatums.",
        "correctAnswer": "All five phrases are urgency, authority, or isolation manipulation tactics",
        "questionText": "Advanced Tone Scan! Read this excerpt from a fake HMRC enforcement email. Select ALL the phrases that use psychological manipulation — urgency, false authority, fear, or isolation tactics:",
        "options": [
            "FINAL WARNING: This is your last opportunity to respond before enforcement action begins",
            "This notice is issued under HMRC Legal Enforcement Division authority — reference TXN-9982",
            "You must take immediate action or face legal prosecution and asset freezing within 48 hours",
            "Do NOT contact your bank or any third party — this is a strictly confidential legal enforcement order",
            "Payment deadline: Tomorrow at 09:00 GMT — absolutely no extensions will be granted under any circumstances"
        ],
        "correctFlags": [
            "FINAL WARNING: This is your last opportunity to respond before enforcement action begins",
            "This notice is issued under HMRC Legal Enforcement Division authority — reference TXN-9982",
            "You must take immediate action or face legal prosecution and asset freezing within 48 hours",
            "Do NOT contact your bank or any third party — this is a strictly confidential legal enforcement order",
            "Payment deadline: Tomorrow at 09:00 GMT — absolutely no extensions will be granted under any circumstances"
        ]
    },

    # Q20 — sequence_builder #2 (Phishing click incident response steps)
    {
        "local_id": 20, "format": "sequence_builder", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "Phishing Click Incident Response — Correct Emergency Sequence",
        "hint": "Disconnecting from the internet is always Step 1 — stop the active data flow before anything else. Preserve evidence before closing. Change passwords LAST and from a clean device — not on the potentially compromised machine!",
        "explain": "Most employees who click a phishing link panic and just close the browser tab, doing nothing else. But phishing links can execute tracking cookies, credential interceptors, and malware droppers in milliseconds. The correct response sequence is engineered to stop ongoing exposure, preserve forensic evidence for IT Security, and ensure passwords are changed from a clean uncompromised device. Sequence discipline is essential for effective incident response.",
        "reveal": "Correct sequence: 1) Disconnect internet immediately (Wi-Fi off / ethernet out) to stop any active data transmission, 2) Do NOT close the browser — preserve the URL as evidence, 3) Screenshot the page and note the URL and time, 4) Report to IT Security with the evidence, 5) Change passwords from a separate CLEAN device — not the potentially compromised one. This sequence maximises damage control and maximises IT's ability to investigate and protect others.",
        "questionText": "Incident Response! You just clicked a phishing link. Your screen shows a fake login page. Arrange these 5 emergency steps in the CORRECT response order to minimise damage:",
        "steps": [
            {"id": "s1", "text": "Disconnect from the internet immediately — turn off Wi-Fi or unplug ethernet to stop data transmission", "correctOrder": 0},
            {"id": "s2", "text": "Do NOT close the browser tab — preserve the malicious URL as evidence for IT Security", "correctOrder": 1},
            {"id": "s3", "text": "Screenshot the phishing page, noting the full URL and exact timestamp", "correctOrder": 2},
            {"id": "s4", "text": "Report to IT Security immediately — provide the URL, screenshot, and how you received the link", "correctOrder": 3},
            {"id": "s5", "text": "Change any potentially compromised passwords from a separate, clean, unaffected device", "correctOrder": 4}
        ]
    },

    # Q21 — file_triage #2 (Advanced Look-Alike Domains: UK bank lookalikes)
    {
        "local_id": 21, "format": "file_triage", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "Advanced Homograph Recognition — UK Bank Lookalike Domains",
        "hint": "Subtle tells: 'lloydsbankonline.co.uk' adds 'online' (Lloyds is lloydsbank.co.uk, not 'lloydsbankonline'). 'rn.barclays.co.uk' — in certain fonts, 'rn' looks identical to 'm' making it look like 'm.barclays.co.uk' — but it is NOT!",
        "explain": "Advanced homograph attacks use two tricks beyond simple character substitution: 1) Appending common words like 'online', 'secure', 'signin', 'mobile' to legitimate brand names to create convincing-sounding subdomains or root domains, and 2) Using character pairs like 'rn' that render visually as 'm' in many common fonts. Both tricks target normal reading speed and pattern recognition rather than individual character scrutiny.",
        "reveal": "EVIL: 'lloydsbankonline.co.uk' (the real Lloyds is lloydsbank.co.uk — 'online' is an added word making it a different registered domain!) and 'rn.barclays.co.uk' (in common sans-serif fonts, 'rn' renders visually like 'm' — but the actual subdomain is 'rn', not 'm'). SAFE: 'lloydsbank.co.uk' (verified real) and 'barclays.co.uk' (verified real). UK banks use simple, canonical domain names without added words or unusual subdomains.",
        "correctAnswer": "SAFE: lloydsbank.co.uk, barclays.co.uk — EVIL: lloydsbankonline.co.uk, rn.barclays.co.uk",
        "questionText": "Advanced Domain Sort! These UK bank domains are harder. Sort SAFE vs EVIL — look at every character and read subdomains carefully against the real company domain!",
        "files": [
            {"id": "f1", "icon": "🏦", "name": "lloydsbank.co.uk — Verified real Lloyds Bank domain", "isMalware": False},
            {"id": "f2", "icon": "💀", "name": "lloydsbankonline.co.uk — Adds 'online' to the real domain — registered separately as a fake!", "isMalware": True},
            {"id": "f3", "icon": "🏦", "name": "barclays.co.uk — Verified real Barclays Bank domain", "isMalware": False},
            {"id": "f4", "icon": "💀", "name": "rn.barclays.co.uk — 'rn' subdomain visually mimics 'm' in sans-serif fonts — NOT a real Barclays subdomain!", "isMalware": True}
        ]
    },

    # Q22 — branching_narratives #2 (Unsolicited password reset email decision)
    {
        "local_id": 22, "format": "branching_narratives", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "Unsolicited Password Reset Email — Correct Decision Path",
        "hint": "Legitimate password reset emails arrive only when YOU initiate them. An unsolicited reset email means either someone is attacking your account — or it is phishing. In BOTH cases, do NOT click the link. Go directly to the service website instead!",
        "explain": "Unsolicited password reset emails are a two-purpose threat: 1) Pure phishing — the 'reset' link goes to a fake page that harvests your current credentials, or 2) Account takeover — a real attacker requested the reset and wants you to click to 'cancel' it (the cancel button may itself be the real reset link). In both cases, the safe action is to navigate directly to the service's real website without using any link from the email.",
        "reveal": "Navigate directly to google.com without using the email link! If someone else requested a Google password reset, the reset token expires without being used — your account remains safe. If it was phishing, you avoided the fake page. Logging into Google directly lets you check Recent Security Activity, see if any suspicious login attempts occurred, and review connected devices — complete situational awareness without any link click risk.",
        "questionText": "Suspicious Reset! An email claiming to be from 'Google Security' says: 'Your Google account password has been reset per your request.' You did NOT request this. What should you do?",
        "options": [
            "Click the Cancel Reset link in the email immediately before the attacker takes over your account",
            "Do nothing — if you did not request it, the reset cannot complete without your active approval",
            "Navigate directly to google.com (typing in a new browser tab), log in, and check Recent Security Activity for suspicious events"
        ],
        "correctAnswer": "Navigate directly to google.com (typing in a new browser tab), log in, and check Recent Security Activity for suspicious events"
    },

    # Q23 — scenario_mcq #2 (Self-signed expired certificate on bank login)
    {
        "local_id": 23, "format": "scenario_mcq", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "SSL Certificate Types — Self-Signed vs CA-Issued Certificates",
        "hint": "A self-signed certificate bypasses all independent verification — ANY attacker can create one in minutes claiming to be any company. An expired certificate shows the site owner has not maintained their security. Both are serious red flags on any login page.",
        "explain": "SSL certificates issued by trusted Certificate Authorities (DigiCert, Let's Encrypt, Comodo) involve independent verification that the site owner controls the domain. A self-signed certificate has no such verification — anyone can generate one instantly claiming any company name. Real banks, healthcare providers, and financial services maintain valid CA-issued certificates at all times. An expired or self-signed certificate on a sensitive login page warrants immediate exit.",
        "reveal": "Leave immediately and report to your bank's real fraud line! A self-signed and expired certificate on a banking login page has ZERO independent trust verification. An attacker can generate this in minutes on any machine. The combination of self-signed + expired is practically definitive proof of a phishing site. Contact your bank using the number on the back of your card or on their official verified website — not any number shown on the suspicious page.",
        "questionText": "SSL Inspector Round 2! On a page that looks like your bank's login, you click the padlock and read: 'Certificate: SELF-SIGNED (not from a trusted Certificate Authority). Status: EXPIRED 3 months ago.' What is the correct action?",
        "options": [
            "Log in normally — HTTPS is present so the connection must be safe regardless of certificate type",
            "Accept the certificate warning — these often appear during legitimate maintenance and upgrade periods",
            "Enter only your sort code to test if the page is real — withhold your full account number",
            "Leave the page immediately and call your bank using the number on the back of your card"
        ],
        "correctAnswer": "Leave the page immediately and call your bank using the number on the back of your card"
    },

    # Q24 — adaptive_inbox (Rapid classification: real vs phishing emails)
    {
        "local_id": 24, "format": "adaptive_inbox", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "Rapid Multi-Email Phishing vs Legitimate Classification",
        "hint": "Check sender domain first (1 second), then subject urgency (1 second), then whether the action requested matches your real relationship with the sender. Phishing emails demand action through links; legitimate notifications just inform.",
        "explain": "Rapid email triage is a professional security skill. The mental algorithm: 1) Sender domain check — does it exactly match the real company domain? 2) Subject urgency scan — is it creating pressure? 3) Action request type — is it asking you to click a link to 'verify', 'confirm', or 'pay'? Most phishing emails fail the first test instantly. Domain mismatches like 'amazon-accounts.net' vs 'amazon.com' can be spotted in under one second.",
        "reveal": "PHISHING: 'Amazon account suspended — amazon-accounts.net' (NOT amazon.com!) and 'DocuSign sign immediately — docusign-alerts.xyz' (NOT docusign.com). SAFE: 'LinkedIn connection requests — linkedin.com' (verified real domain) and 'Apple receipt — email.apple.com' (apple.com subdomain — verified real). The two phishing emails both use urgent subject lines AND non-matching domains — double confirmation.",
        "questionText": "Inbox Triage! Four emails need rapid classification. Swipe each one as SAFE or PHISH before the timer counts down!",
        "emails": [
            {"id": "e1", "subject": "You have 3 new connection requests on LinkedIn this week", "sender": "notifications@linkedin.com", "isPhish": False},
            {"id": "e2", "subject": "URGENT: Your Amazon account has been suspended — verify immediately", "sender": "no-reply@amazon-accounts.net", "isPhish": True},
            {"id": "e3", "subject": "Your receipt for App Store purchase — £2.99 Spotify Premium", "sender": "no_reply@email.apple.com", "isPhish": False},
            {"id": "e4", "subject": "DocuSign: Please sign your URGENT document — expires in 1 hour", "sender": "sign@docusign-alerts.xyz", "isPhish": True}
        ]
    },

    # Q25 — scavenger_hunt (Find ALL phishing red flags on a complete email mockup)
    {
        "local_id": 25, "format": "scavenger_hunt", "difficulty": "medium",
        "gameName": "phishing", "game_key": "phishing", "level_name": "medium",
        "concept": "Comprehensive Multi-Layer Phishing Email Analysis",
        "hint": "A trained analyst checks multiple layers: sender domain, urgency language, salutation, link destination on hover, and any instruction that blocks normal verification. Find all five red flags on this email!",
        "explain": "Expert-level phishing detection requires simultaneous multi-layer checking. The envelope (sender domain), content (urgency + authority), technical elements (link destination), and call-to-action analysis together create a complete threat picture. Real security professionals rarely rely on just one indicator — confirmed phishing emails almost always fail multiple checks simultaneously.",
        "reveal": "All five are red flags: 1) Sender 'lloyds-online-secure.com' (NOT lloydsbank.co.uk — the root domain is completely different!), 2) Subject 'SUSPENDED WITHIN 4 HOURS' (countdown urgency!), 3) 'Dear Valued Customer' (your real bank uses your full name!), 4) Hover link goes to 'lloyds-secure-verify.ru' (Russian domain — .ru is never a UK bank domain!), 5) 'Do not call Lloyds Bank' instruction (classic isolation tactic preventing verification!). Any TWO of these confirm phishing. All five together make this textbook.",
        "correctAnswer": "Click all 5: suspicious sender domain, urgency countdown, generic salutation, hover link to .ru domain, isolation instruction",
        "questionText": "Full Phishing Analysis! This email is displayed on screen. A trained analyst would spot at least 5 red flags. Click ALL the phishing indicators you can find!",
        "objects": [
            {"id": "o1", "icon": "💀", "label": "FROM: security@lloyds-online-secure.com (NOT lloydsbank.co.uk!)", "isRedFlag": True, "top": "5%", "left": "5%"},
            {"id": "o2", "icon": "💀", "label": "SUBJECT: Your account will be SUSPENDED WITHIN 4 HOURS", "isRedFlag": True, "top": "18%", "left": "5%"},
            {"id": "o3", "icon": "💀", "label": "Salutation: Dear Valued Customer (your real bank uses your full name!)", "isRedFlag": True, "top": "35%", "left": "5%"},
            {"id": "o4", "icon": "💀", "label": "Hover link reveals: lloyds-secure-verify.ru/login (Russian .ru domain — never a UK bank!)", "isRedFlag": True, "top": "55%", "left": "5%"},
            {"id": "o5", "icon": "💀", "label": "Instruction at bottom: Do NOT call Lloyds Bank about this message (isolation tactic!)", "isRedFlag": True, "top": "75%", "left": "5%"}
        ]
    }

]

result = col.insert_many(questions)
count = col.count_documents({'game_key': 'phishing', 'level_name': 'medium'})
print("Inserted:", len(result.inserted_ids), "phishing medium questions")
print("Total phishing medium in DB:", count)
print("\nFormat order:")
prev = ""
all_ok = True
from collections import Counter
fmt_counts = Counter(q['format'] for q in questions)
for i, q in enumerate(questions):
    dup = " <<< CONSECUTIVE!" if q['format'] == prev else ""
    if dup: all_ok = False
    print(f"  Q{q['local_id']:2}: {q['format']}{dup}")
    prev = q['format']
print("\nFormat counts:", dict(sorted(fmt_counts.items())))
over = {f: c for f, c in fmt_counts.items() if c > 2}
if over: print("OVER LIMIT:", over)
elif all_ok: print("\nAll good — no consecutive duplicates, all formats ≤ 2!")
client.close()
