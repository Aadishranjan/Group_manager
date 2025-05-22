import random
import logging
from telegram import Update
from telegram.ext import ContextTypes

photo_urls = [
    "https://i.ibb.co/r2rCVPMj/welcome.webp",
    "https://i.ibb.co/WvSptPY5/welcome2.webp"
]

async def delete_message(context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = context.job.data["chat_id"]
        message_id = context.job.data["message_id"]
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        logging.warning(f"Failed to delete welcome message: {e}")

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        for member in update.message.new_chat_members:
            name = member.full_name
            selected_photo = random.choice(photo_urls)
            caption = f"👋 Welcome [{name}](tg://user?id={member.id}) to *{update.effective_chat.title}*!\n\nEnjoy your stay and follow the group rules."

            sent = await update.message.reply_photo(
                photo=selected_photo,
                caption=caption,
                parse_mode="Markdown"
            )

            # Schedule deletion after 5 minutes (300 seconds)
            context.job_queue.run_once(
                delete_message,
                when=60,
                data={"chat_id": sent.chat_id, "message_id": sent.message_id}
            )

    except Exception as e:
        logging.error(f"Failed to send or schedule welcome message deletion: {e}")