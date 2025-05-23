from telegram import Update
from telegram.ext import ContextTypes
import re

# Regex to detect URLs
URL_PATTERN = re.compile(r"https?://|www\.")

async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    if message and (message.text or message.caption) and message.from_user:
        user = message.from_user

        # Check if message contains a link
        has_link = URL_PATTERN.search((message.text or message.caption).lower())

        # Check if sender is a bot
        if user.is_bot and has_link:
            try:
                await message.delete()
                print(f"Deleted link from bot: @{user.username or 'Unknown'}")
            except Exception as e:
                print(f"Failed to delete message: {e}")