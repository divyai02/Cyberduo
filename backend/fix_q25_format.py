from dotenv import load_dotenv
import os
load_dotenv()
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGO_URI'))
col = client['cyberduo']['questions']

# Fix Q25: change digital_whodunnit -> scenario_mcq
# The digital_whodunnit renderer expects email headers (from/spf/dkim) but our Q25 uses a timeline
# Converting to scenario_mcq which renders options perfectly and already has the right correctAnswer

result = col.update_one(
    {'game_key': 'scams', 'level_name': 'beginner', 'local_id': 25},
    {'$set': {
        'format': 'scenario_mcq',
        'questionText': "Scam Crime Scene! Maria sold her bicycle online for £200. A buyer called 'Tom' sent a cheque for £2,000 'by mistake' and asked her to bank it and transfer back the £1,800 difference. Maria agreed, transferred the money, and Tom collected the bicycle. Three weeks later, her bank reversed £2,000 from her account — the cheque was counterfeit. At what point did Maria make the critical mistake that caused her to lose £1,800?",
    }}
)
print("Updated Q25:", result.modified_count, "document")

# Verify
q25 = col.find_one({'game_key': 'scams', 'level_name': 'beginner', 'local_id': 25})
print("Q25 format is now:", q25['format'])
print("Q25 options:", q25.get('options', []))
print("Q25 correctAnswer:", q25.get('correctAnswer', ''))

client.close()
