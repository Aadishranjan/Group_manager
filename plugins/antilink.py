from telegram import Update, ChatMember
from telegram.ext import ContextTypes
import re

URL_PATTERN = re.compile(r"https?://|www\.")

async def is_user_admin(update: Update, user_id: int) -> bool:
    try:
        chat_member = await update.effective_chat.get_member(user_id)
        return chat_member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return False

async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    if not message or not message.from_user:
        return

    user = message.from_user
    text = message.text or message.caption or ""
    has_link = URL_PATTERN.search(text.lower())

    if has_link:
        is_admin = await is_user_admin(update, user.id)
        if not is_admin:
            try:
                await message.delete()
                print(f"Deleted message with link from: @{user.username or user.id}")
            except Exception as e:
                print(f"Failed to delete message: {e}")
