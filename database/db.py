from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["group_manager"]
afk_collection = db["afk"]
users_collection = db["users"]
warn_collection = db["warn"]

async def save_chat(chat_id, chat_type, title):
    users_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"chat_type": chat_type, "title": title}},
        upsert=True
    )

def get_all_chat_ids():
    return [doc["chat_id"] for doc in db["users"].find({}, {"chat_id": 1})]    
    
    
print("mongodb connected")
