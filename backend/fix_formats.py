from dotenv import load_dotenv
import os
load_dotenv()
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGO_URI'))
col = client['cyberduo']['questions']

# Fix Q22: digital_whodunnit tries to read currentQ.emails but we stored currentQ.headers
# -> Change to scenario_mcq (already renders correctly, uses options + correctAnswer)
col.update_one(
    {'game_key': 'malware', 'level_name': 'beginner', 'local_id': 22},
    {'$set': {
        'format': 'scenario_mcq',
        'questionText': 'Malware Crime Scene! Read this infection timeline and identify the EXACT action that let the malware in. Which log entry was the initial infection entry point?',
        'scenario': (
            '9:24 AM — Email received from: totallyreal-offers@free-stuff.xyz with attachment free_gift_voucher.pdf.exe\n'
            '9:26 AM — User OPENED file: free_gift_voucher.pdf.exe (file executed code on the system)\n'
            '9:27 AM — Outgoing connection: PC connected to c2server.darkweb.io (malware phoned home!)\n'
            '9:30 AM — Windows update check: microsoft.com — normal scheduled activity'
        )
    }}
)

# Fix Q23: traffic_triage HAS validation logic but NO render case in GameScreen switch
# -> Change to file_triage which renders perfectly (already used in Q1 and Q8)
col.update_one(
    {'game_key': 'malware', 'level_name': 'beginner', 'local_id': 23},
    {'$set': {
        'format': 'file_triage',
        'questionText': 'Network Traffic Scan! Your security tool flagged outgoing connections from your PC. Some are normal system traffic, others are malware secretly sending your data. Mark each connection as SAFE or MALWARE:',
        'files': [
            {'id': 'f1', 'icon': '💀', 'name': 'keylogger-upload.xyz — POST /upload?keys=yourpassword (stealing your keystrokes!)', 'isMalware': True},
            {'id': 'f2', 'icon': '📄', 'name': 'microsoft.com — GET /windowsupdate — normal scheduled Windows update check', 'isMalware': False},
            {'id': 'f3', 'icon': '💀', 'name': 'cryptominer-pool.darkweb.io — mining protocol using YOUR CPU for attacker profit!', 'isMalware': True}
        ],
        # Remove traffic field and keep correctAnswer
        'correctAnswer': 'MALWARE: keylogger-upload.xyz, cryptominer-pool.darkweb.io — SAFE: microsoft.com'
    }}
)
# Also unset the old 'traffic' field so it's clean
col.update_one(
    {'game_key': 'malware', 'level_name': 'beginner', 'local_id': 23},
    {'$unset': {'traffic': ''}}
)

# Also check phishing Q1 (digital_whodunnit) and Q13 (traffic_triage) 
# Q1 phishing uses headers array, Q13 uses traffic array
# Fix phishing Q1 digital_whodunnit - it tries to read currentQ.emails but we have currentQ.headers
col.update_one(
    {'game_key': 'phishing', 'level_name': 'beginner', 'local_id': 1},
    {'$set': {
        'format': 'scenario_mcq',
        'questionText': 'Email Header Murder Mystery! A suspicious PayPal email arrived. The technical email headers reveal a shocking forgery. Which field proves this email is FAKE and NOT from PayPal?',
        'scenario': (
            'DISPLAY NAME: PayPal Security <paypal-security@mail-alert.ru>\n'
            'TO: you@yourmail.com\n'
            'SUBJECT: Your PayPal account is limited!\n'
            'DATE: Mon, 10 Apr 2026 at 03:22 AM\n'
            'RETURN-PATH: paypal-security@mail-alert.ru'
        )
    }}
)

# Fix phishing Q13 traffic_triage - no render case exists
col.update_one(
    {'game_key': 'phishing', 'level_name': 'beginner', 'local_id': 13},
    {'$set': {
        'format': 'file_triage',
        'questionText': 'Network Traffic Inspector! After clicking a suspicious email link, these 3 outgoing connections appeared in the security log. Some are phishing attacks stealing your data. Mark each as SAFE or MALWARE:',
        'files': [
            {'id': 'f1', 'icon': '💀', 'name': 'steal-creds.xyz — POST /collect?user=you&pass=**** (stealing your login credentials!)', 'isMalware': True},
            {'id': 'f2', 'icon': '📄', 'name': 'microsoft.com — GET /updates/win11-patch — normal Windows update download', 'isMalware': False},
            {'id': 'f3', 'icon': '💀', 'name': 'tracking.phish-ops.net — GET /beacon?id=victim_001 (reporting you to the attacker!)', 'isMalware': True}
        ],
        'correctAnswer': 'MALWARE: steal-creds.xyz, tracking.phish-ops.net — SAFE: microsoft.com'
    }}
)
col.update_one(
    {'game_key': 'phishing', 'level_name': 'beginner', 'local_id': 13},
    {'$unset': {'traffic': ''}}
)

print("Fixed formats:")
for game, lid, expected_format in [('malware', 22, 'scenario_mcq'), ('malware', 23, 'file_triage'), ('phishing', 1, 'scenario_mcq'), ('phishing', 13, 'file_triage')]:
    q = col.find_one({'game_key': game, 'level_name': 'beginner', 'local_id': lid})
    actual = q.get('format', 'MISSING')
    status = 'OK' if actual == expected_format else 'FAIL'
    print(f"  [{status}] {game} Q{lid}: format = {actual}")

client.close()
