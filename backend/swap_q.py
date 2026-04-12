from dotenv import load_dotenv
import os
load_dotenv()
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGO_URI'))
col = client['cyberduo']['questions']

# Swap local_id 4 (deepfake_detection) <-> local_id 10 (sequence_builder)
# Step 1: move Q4 to temp id 999
col.update_one(
    {'game_key': 'phishing', 'level_name': 'beginner', 'local_id': 4},
    {'$set': {'local_id': 999}}
)
# Step 2: move Q10 (sequence_builder) to position 4
col.update_one(
    {'game_key': 'phishing', 'level_name': 'beginner', 'local_id': 10},
    {'$set': {'local_id': 4}}
)
# Step 3: move temp (old Q4 deepfake) to position 10
col.update_one(
    {'game_key': 'phishing', 'level_name': 'beginner', 'local_id': 999},
    {'$set': {'local_id': 10}}
)

# Verify
docs = list(col.find(
    {'game_key': 'phishing', 'level_name': 'beginner'},
    {'local_id': 1, 'format': 1, '_id': 0}
).sort('local_id', 1))

for d in docs:
    print('id=' + str(d.get('local_id', '?')).rjust(2) + '  format=' + str(d.get('format', '?')))

print('Total:', len(docs))
client.close()
