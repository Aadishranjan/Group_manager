from telegram import Update, User
from telegram.ext import ContextTypes, CommandHandler
from database.warn_db import add_warn, reset_warns

async def warn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user: User = None
    chat_id = update.effective_chat.id

    # Case 1: Used as a reply
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user

    # Case 2: Used with username/user_id
    elif context.args:
        try:
            arg = context.args[0]
            if arg.startswith("@"):
                arg = arg[1:]
            user = await context.bot.get_chat_member(chat_id, arg)
            user = user.user
        except Exception as e:
            await update.message.reply_text("Couldn't find that user.")
            return
    else:
        await update.message.reply_text("Tag a user and write /warn to warn.")
        return

    warn_count = add_warn(user.id, chat_id)

    if warn_count >= 3:
        await context.bot.ban_chat_member(chat_id, user.id)
        reset_warns(user.id, chat_id)
        await update.message.reply_text(
            f"{user.mention_html()} was banned after 3 warnings!", parse_mode='HTML'
        )
    else:
        await update.message.reply_text(
            f"⚠️ Warning {warn_count}/3 issued to {user.mention_html()}", parse_mode='HTML'
        )

def warn_handlers():
    return [CommandHandler("warn", warn_user)]