import json
import traceback

filepath = r'frontend\src\data\GameQuestions.json'
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

for i, q in enumerate(data['phishing']['beginner']):
    f = q['format']
    try:
        if f=='svg_code_inspection' and 'codeLines' not in q: print('Fail', i, f, 'missing codeLines')
        if f=='branching_narratives' and 'options' not in q: print('Fail', i, f, 'missing options')
        if f=='omni_threat_chains' and ('channels' not in q or 'parts' not in q.get('channels', [{}])[0]): print('Fail', i, f, 'missing channels')
        if f=='capture_the_flag' and 'objects' not in q: print('Fail', i, f, 'missing objects')
        if f=='adaptive_inbox' and 'emails' not in q: print('Fail', i, f, 'missing emails')
        if f=='the_imposter' and ('messages' not in q or 'options' not in q): print('Fail', i, f, 'missing messages/options')
        if f=='escape_rooms' and 'cipherText' not in q: print('Fail', i, f, 'missing cipherText')
        if f=='deepfake_detection' and ('audioTranscript' not in q or 'options' not in q): print('Fail', i, f, 'missing deepfake data')
        if f=='spot_the_difference' and ('urlReal' not in q or 'options' not in q): print('Fail', i, f, 'missing spot_the_diff data')
        if f=='digital_whodunnit' and 'emails' not in q: print('Fail', i, f, 'missing emails')
        if f=='adversary_roleplay' and 'assets' not in q: print('Fail', i, f, 'missing assets')
        if f=='quishing_drills' and 'decodedURL' not in q: print('Fail', i, f, 'missing decodedURL')
        if f in ['phish_a_friend', 'resource_management', 'cyber_snakes_ladders'] and 'options' not in q: print('Fail', i, f, 'missing options')
    except Exception as e:
        print('Exception on', i, f, e)
print('Validation done')
