from pymongo import ReturnDocument

try:
    print("ReturnDocument.BEFORE:", ReturnDocument.BEFORE)
    print("ReturnDocument.AFTER:", ReturnDocument.AFTER)
    print("True evaluated to enum?:", True == ReturnDocument.AFTER)
except Exception as e:
    print("Error:", e)
