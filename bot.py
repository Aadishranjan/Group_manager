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
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN, ADMIN_ID
from plugins.function import start
from plugins.group import welcome_new_member

# Global scheduler
scheduler = AsyncIOScheduler(timezone=timezone.utc)

async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "Available commands:\n/start - Start the bot\n/help - Help info"
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
        app.add_handler(CallbackQueryHandler(help_callback, pattern="^help_command$"))
        app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))

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
    main()