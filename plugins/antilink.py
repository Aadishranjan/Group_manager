from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
import re

# Regex to detect URLs
URL_PATTERN = re.compile(r"https?://|www\.")

async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    if message and message.text:
        if URL_PATTERN.search(message.text.lower()):
            try:
                await message.delete()
                print(f"Deleted message with link from {message.from_user.username or message.from_user.id}")
            except Exception as e:
                print(f"Failed to delete message: {e}")