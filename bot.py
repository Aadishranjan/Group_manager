# --- Flask server for Render/Heroku ---
from flask import Flask
import threading
import os

flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot is running!"

def run_server():
    port = int(os.getenv("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

# --- Telegram Bot Setup ---
import asyncio
import logging
import sys
import traceback
from datetime import timezone
from telegram import Update, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
    ChatMemberHandler,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import BOT_TOKEN, ADMIN_ID
from plugins.function import start
from plugins.group import welcome_new_member
from plugins import mute
from plugins.antilink import delete_links
from plugins.warn import warn_handlers
from plugins.goodbye import goodbye_handler
from plugins.broadcast import broadcast

# Global scheduler
scheduler = AsyncIOScheduler(timezone=timezone.utc)

async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/broadcast - Only bot admin is allowed\n"
        "/ban - Ban a user\n"
        "/unban - Unban a user\n"
        "/mute - Mute a user\n"
        "/unmute - Unmute a user\n"
        "/warn - Tag a user or use /warn @username to warn them\n"
        "Users will be banned after 3 warnings."
    )

async def on_startup(application: Application):
    scheduler.start()
    application.job_queue.scheduler = scheduler
    print("✅ Scheduler started.")

def main():
    try:
        app = Application.builder().token(BOT_TOKEN).post_init(on_startup).build()

        # Handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("mute", mute.mute_user))
        app.add_handler(CommandHandler("unmute", mute.unmute_user))
        app.add_handler(CommandHandler("ban", mute.ban_user))
        app.add_handler(CommandHandler("unban", mute.unban_user))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), delete_links))
        app.add_handler(MessageHandler(filters.Caption(), delete_links))
        app.add_handler(CallbackQueryHandler(help_callback, pattern="^help_command$"))
        app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
        app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, goodbye_handler))
        app.add_handler(CommandHandler("broadcast", broadcast))
        for handler in warn_handlers():
            app.add_handler(handler)

        print("✅ Bot is running...")
        app.run_polling()

    except Exception:
        error_text = f"🚨 BOT CRASHED!\n\n{traceback.format_exc()}"
        logging.error(error_text)

        async def notify_admin():
            try:
                bot = Bot(BOT_TOKEN)
                await bot.send_message(chat_id=ADMIN_ID, text=error_text)
            except Exception as notify_err:
                print(f"Error notifying admin: {notify_err}")

        asyncio.run(notify_admin())
        sys.exit(1)

if __name__ == "__main__":
    # Run Flask server in background for Render/Heroku
    threading.Thread(target=run_server).start()
    main()