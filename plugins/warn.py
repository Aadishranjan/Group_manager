from telegram import Update, User, ChatMember
from telegram.ext import ContextTypes, CommandHandler
from database.warn_db import add_warn, reset_warns

# Helper to check if command issuer is admin
async def is_user_admin(update: Update, user_id: int) -> bool:
    try:
        member = await update.effective_chat.get_member(user_id)
        return member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]
    except:
        return False

async def warn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_user_admin(update, update.effective_user.id):
        await update.message.reply_text("Only admins can issue warnings.")
        return

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
            member = await context.bot.get_chat_member(chat_id, arg)
            user = member.user
        except Exception:
            await update.message.reply_text("Couldn't find that user.")
            return
    else:
        await update.message.reply_text("Tag a user or reply to them with /warn.")
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
