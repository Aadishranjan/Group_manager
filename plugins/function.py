from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import random, logging
from database.db import save_chat  # sync function

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_urls = [
        "https://i.ibb.co/fPxCsZQ/welcome3.webp",
        "https://i.ibb.co/Xf2xC19c/welcome.webp",
        "https://i.ibb.co/ZpxF6MMQ/welcome4.webp",
        "https://i.ibb.co/m59xPfHn/welcome2.webp"
    ]
    selected_photo = random.choice(photo_urls)

    # Save chat or user id in broadcast
    chat = update.effective_chat
    if chat.type in ["group", "supergroup"]:
        save_chat(chat.id, "group", chat.title)  # ⛔ Don't await
    elif chat.type == "private":
        save_chat(chat.id, "private", update.effective_user.full_name)

    caption = (
        "👋 **Welcome to Group Manager Bot!**\n\n"
        "I can help you manage your Telegram groups with features like:\n"
        "• Auto-moderation\n"
        "• Welcome messages\n"
        "• Anti-link protection\n"
        "• Mute, ban, warn system\n\n"
        "🤖 Developed and managed by [Aadish](https://t.me/aadish555)\n"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Me To Your Group", url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [InlineKeyboardButton("📚 Help Command", callback_data="help_command")]
    ])

    try:
        await update.message.reply_photo(
            photo=selected_photo,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=keyboard
        )
    except Exception as e:
        logging.error(f"Failed to send welcome image: {e}")
        await update.message.reply_text("⚠️ Failed to send welcome image. Please contact admin.")