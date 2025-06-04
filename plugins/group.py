import random
import logging
from telegram import Update
from telegram.ext import ContextTypes
from database.db import user_data

photo_urls = [
    "https://i.ibb.co/fPxCsZQ/welcome3.webp",
    "https://i.ibb.co/Xf2xC19c/welcome.webp",
    "https://i.ibb.co/ZpxF6MMQ/welcome4.webp",
    "https://i.ibb.co/m59xPfHn/welcome2.webp"
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
            await user_data(user_id=member.id, username=member.username, full_name=member.full_name)
            
            name = member.full_name.replace("[", "\").replace("]", "\")
            user_link = f"[{name}](tg://user?id={member.id})"
            group_name = update.effective_chat.title.replace("[", "\").replace("]", "\")

            selected_photo = random.choice(photo_urls)

            caption = (
                f"Hᴇʏ ᴅᴇᴀʀ {user_link}, Wᴇʟᴄᴏᴍᴇ ᴛᴏ *{group_name}* Gʀᴏᴜᴘ.\n\n"
                f"┏━━━━»»❀\n"
                f"♛ ɴᴀᴍᴇ : {name}\n"
                f"⍟ I'ᴅ : `{member.id}`\n"
                f"┕━━━━━━━━━━━━»»❀"
            )

            sent = await update.message.reply_photo(
                photo=selected_photo,
                caption=caption,
                parse_mode="Markdown"
            )

            # Schedule deletion after 5 minutes
            context.job_queue.run_once(
                delete_message,
                when=300,
                data={"chat_id": sent.chat_id, "message_id": sent.message_id}
            )

    except Exception as e:
        logging.error(f"Failed to send or schedule welcome message deletion: {e}")
