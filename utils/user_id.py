from database.db import get_user_from_db

async def get_user_id_from_username(username: str):
    if username.startswith("@"):
        username = username[1:]

    db_user = get_user_from_db(username)
    if db_user:
        return db_user.get("user_id")
    return None