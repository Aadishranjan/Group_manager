from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database.db import get_all_chat_ids  # You’ll create this
import logging

# Replace with your own Telegram user ID
ADMIN_IDS = [5782873898]

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return

    if not context.args:
        await update.message.reply_text("❗ Please provide a broadcast message or reply to an image with a caption.")
        return

    # Fetch all saved chat_ids (users + groups)
    chat_ids = get_all_chat_ids()

    count = 0
    for chat_id in chat_ids:
        try:
            if update.message.photo:
                # Broadcast image with caption
                file_id = update.message.photo[-1].file_id
                caption = " ".join(context.args)
                await context.bot.send_photo(chat_id=chat_id, photo=file_id, caption=caption)
            else:
                # Broadcast plain text
                message = " ".join(context.args)
                await context.bot.send_message(chat_id=chat_id, text=message)
            count += 1
        except Exception as e:
            logging.warning(f"Failed to send to {chat_id}: {e}")

    await update.message.reply_text(f"✅ Broadcast sent to {count} chats.")