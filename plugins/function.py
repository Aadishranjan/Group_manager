import random
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_urls = [
        "https://i.ibb.co/r2rCVPMj/welcome.webp",
        "https://i.ibb.co/WvSptPY5/welcome2.webp"
    ]
    selected_photo = random.choice(photo_urls)

    caption = (
        "👋 **Welcome to Group Manager Bot!**\n\n"
        "I can help you manage your Telegram groups with features like:\n"
        "• Auto-moderation\n"
        "• Welcome messages\n"
        "• Anti-link protection\n"
        "• Mute, ban, warn system\n\n"
        "Use the buttons below to get started!"
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