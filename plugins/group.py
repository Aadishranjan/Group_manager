import logging
from telegram import Update
from telegram.ext import ContextTypes
from database.db import user_data

# MarkdownV2 escape helper
def escape_md(text: str) -> str:
    escape_chars = r"\_*[]()~`>#+-=|{}.!<>"
    return ''.join(f"\\{c}" if c in escape_chars else c for c in text)

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message or not update.message.new_chat_members:
            return

        for member in update.message.new_chat_members:
            user_data(user_id=member.id, username=member.username, full_name=member.full_name)

            full_name = escape_md(member.full_name or "User")
            group_name = escape_md(update.effective_chat.title or "Group")
            user_link = f"[{full_name}](tg://user?id={member.id})"

            message = f"ʜɪɪ {user_link}\nᴡᴇʟᴄᴏᴍᴇ ᴛᴏ *{group_name}*"

            await update.message.reply_text(
                text=message,
                parse_mode="MarkdownV2"
            )

    except Exception as e:
        logging.error(f"Failed to send welcome message: {e}")