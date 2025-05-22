import os
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode

GOODBYE_GIF_PATH = "goodbye.gif"

async def goodbye_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.left_chat_member:
        user = update.message.left_chat_member
        name = user.full_name.replace('[', '\').replace(']', '\')
        username = user.username

        if username:
            mention = f"[{name}](https://t.me/{username})"
        else:
            mention = name  # fallback if no username

        text = f"Gᴏᴏᴅ Bʏᴇ {mention} Nᴏ Oɴᴇ Wɪʟʟ Mɪss Yᴏᴜ 💕"

        if os.path.exists(GOODBYE_GIF_PATH):
            with open(GOODBYE_GIF_PATH, 'rb') as gif:
                await update.message.reply_animation(
                    animation=gif,
                    caption=text,
                    parse_mode=ParseMode.MARKDOWN_V2
                )
        else:
            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN_V2)