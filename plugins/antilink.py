from telegram import Update
from telegram.ext import ContextTypes
import re

# Only these bots/users will have their messages checked for links
ALLOWED_USERNAMES = {"@Resso_singing_bot", "@YaeMiko_Roxbot", "@FSCGroupHelpBot", "@TheChampuBot", "@ProtectronBot", "@KeyaMusicBot", "@MediaGuardianBot"}

# Regex to detect URLs
URL_PATTERN = re.compile(r"https?://|www\.")

async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    if message and message.text and message.from_user:
        username = f"@{message.from_user.username}" if message.from_user.username else None

        if username in ALLOWED_USERNAMES and URL_PATTERN.search(message.text.lower()):
            try:
                await message.delete()
                print(f"Deleted link from {username}")
            except Exception as e:
                print(f"Failed to delete message: {e}")