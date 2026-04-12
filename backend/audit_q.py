from dotenv import load_dotenv; import os; load_dotenv()
from pymongo import MongoClient
client = MongoClient(os.getenv('MONGO_URI'))
col = client['cyberduo']['questions']

docs = list(col.find({'game_key': 'phishing', 'level_name': 'beginner'}, {'local_id': 1, 'format': 1, '_id': 0}).sort('local_id', 1))
for d in docs:
    print("id=" + str(d.get('local_id', '?')).rjust(2) + "  format=" + str(d.get('format', '?')))
print("Total: " + str(len(docs)))
client.close()
