import json
import random

filepath = r'frontend\src\data\GameQuestions.json'
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

phishing_hints = {
    "adaptive_inbox": "Check the sender's actual address, not just the display name.",
    "spot_the_difference": "Look closely at the URL structure; typosquatting is a common tactic.",
    "svg_code_inspection": "Search for embedded scripts or foreign domains executing within the image code.",
    "digital_whodunnit": "Verify authentications like SPF and DKIM to uncover spoofed domains.",
    "escape_rooms": "Apply the specified cryptographic offset to the characters.",
    "cyber_snakes_ladders": "Identify the emotional trigger or financial threat being leveraged.",
    "resource_management": "Prioritize security protocols over convenience when handling sensitive data.",
    "deepfake_detection": "Look for unnatural artifacts like mismatched lip-sync or robotic lighting.",
    "capture_the_flag": "Hover over elements to uncover obscured links or suspicious metadata.",
    "branching_narratives": "Assess out-of-band verification paths instead of trusting the immediate channel.",
    "quishing_drills": "QR codes can mask malicious destinations just like shortened links.",
    "omni_threat_chains": "Track the payload sequence across multiple platforms to find the origin.",
    "the_imposter": "Look for inconsistencies in tone, urgency, or unusual requests from the 'colleague'.",
    "adversary_roleplay": "Think like an attacker: high urgency limits critical thinking.",
    "phish_a_friend": "Personalized lures (Spear Phishing) are often built on public social media data."
}

for idx, q in enumerate(data['phishing']['beginner']):
    fmt = q['format']
    
    # Set dynamic hint
    q['hint'] = phishing_hints.get(fmt, "Verify the source independently before trusting the prompt.")
    
    # Set dynamic explain based on the format and question text
    if fmt == 'spot_the_difference':
        q['explain'] = f"The URL {q.get('urlFake')} utilizes character substitution to mimic the legitimate {q.get('brandName')} portal."
    elif fmt == 'svg_code_inspection':
        q['explain'] = "Attackers embed malicious <script> tags inside SVG vector files to bypass standard image filters."
    elif fmt == 'digital_whodunnit':
        q['explain'] = "A failed SPF or DKIM check proves the email did not originate from the authorized domain."
    elif fmt == 'escape_rooms':
        q['explain'] = f"The ciphertext '{q.get('cipherText')}' shifts backwards alphabetically by the cipher rotation to reveal the true flag."
    elif fmt == 'deepfake_detection':
        q['explain'] = "Deepfakes often fail at subtle human movements and voice modulation under unexpected conditions."
    elif fmt == 'capture_the_flag':
        q['explain'] = "Hidden elements on legitimate-looking interfaces often conceal credential-harvesting endpoints."
    elif fmt == 'branching_narratives':
        q['explain'] = "Social engineering hinges on false urgency. Verifying via an alternative channel neutralizes the pressure."
    elif fmt == 'quishing_drills':
        q['explain'] = f"The scanned destination ({q.get('decodedURL')}) circumvents mobile security by initiating direct device actions."
    elif fmt == 'the_imposter':
        q['explain'] = "Business Email Compromise (BEC) often leverages compromised internal accounts to request unusual wire transfers."
    elif fmt == 'adversary_roleplay':
        q['explain'] = "High-ROI phishing campaigns balance the cost of customized assets against the likelihood of psychological manipulation."
    else:
        q['explain'] = "Attackers manipulate human psychology and technical trust to bypass authentication protocols."

    # Set dynamic reveal
    q['reveal'] = f"Zero-Trust Protocol: Never assume systemic trust for {fmt.replace('_', ' ')} elements."

    # Fix Duplicates
    if q['id'] == 6 and fmt == 'cyber_snakes_ladders':
        q['scenario'] = "An email claims you won the lottery, but asks for a $50 processing fee."
        q['explain'] = "Advance Fee Fraud targets greed by requiring a small upfront payment for a non-existent larger payout."
    if q['id'] == 17 and fmt == 'cyber_snakes_ladders':
        q['scenario'] = "The 'IT Desk' demands you click a link immediately to prevent account deletion."
        q['options'] = ["IT Impersonation", "Standard Password Reset", "Routine Audit"]
        q['correctAnswer'] = "IT Impersonation"
        q['explain'] = "Impersonating authority figures (like IT admins) creates a power dynamic that forces rapid compliance."

    # Verify correctAnswer exists for UI rendering if it's not a complex object
    if 'correctAnswer' not in q and 'emails' not in q and 'objects' not in q and 'assets' not in q:
        q['correctAnswer'] = q.get('options', [''])[0]

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("GameQuestions.json updated perfectly!")
