from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["group_manager"]
afk_collection = db["afk"]
warn_collection = db["warn"]
print("mongodb connected")