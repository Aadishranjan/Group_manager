from .db import warn_collection

def add_warn(user_id: int, chat_id: int) -> int:
    user_data = warn_collection.find_one({"user_id": user_id, "chat_id": chat_id})
    if user_data:
        new_count = user_data["count"] + 1
        warn_collection.update_one(
            {"user_id": user_id, "chat_id": chat_id},
            {"$set": {"count": new_count}}
        )
    else:
        new_count = 1
        warn_collection.insert_one({"user_id": user_id, "chat_id": chat_id, "count": new_count})
    return new_count

def reset_warns(user_id: int, chat_id: int):
    warn_collection.delete_one({"user_id": user_id, "chat_id": chat_id})
    
def remove_warn(user_id: int, chat_id: int) -> int:
    user_data = warn_collection.find_one({"user_id": user_id, "chat_id": chat_id})
    if user_data:
        current_count = user_data.get("count", 0)
        new_count = max(0, current_count - 1)
        warn_collection.update_one(
            {"user_id": user_id, "chat_id": chat_id},
            {"$set": {"count": new_count}}
        )
    else:
        new_count = 0
        warn_collection.insert_one({"user_id": user_id, "chat_id": chat_id, "count": new_count})
    return new_count