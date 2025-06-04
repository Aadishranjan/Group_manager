from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["group_manager"]

# Collections
broadcast_collection = db["broadcast"]
users_collection = db["users"]
warn_collection = db["warn"]


# Save chat (for private or group)
def save_chat(chat_id: int, chat_type: str, name: str):
    broadcast_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"chat_type": chat_type, "name": name}},
        upsert=True
    )

# Get all chat IDs for broadcast
def get_all_chat_ids():
    return [doc["chat_id"] for doc in broadcast_collection.find({}, {"chat_id": 1})]

# Save user data if not already present
def user_data(user_id: int, username: str, full_name: str):
    user_info = {
        "user_id": user_id,
        "username": username,
        "full_name": full_name
    }
    existing = users_collection.find_one({"user_id": user_id})
    if not existing:
        users_collection.insert_one(user_info)

# Get user from DB by username
def get_user_from_db(username: str):
    return users_collection.find_one({"username": username})

print("MongoDB connected")