from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB_NAME, MONGO_LOGINS_COLLECTION, MONGO_ALERTS_COLLECTION

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
logins_collection = db[MONGO_LOGINS_COLLECTION]
alerts_collection = db[MONGO_ALERTS_COLLECTION]