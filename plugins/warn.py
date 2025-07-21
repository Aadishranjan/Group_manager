from telegram import Update, ChatMember, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database.warn_db import add_warn, reset_warns, remove_warn
from database.db import get_user_from_db
from utils.user_id import get_user_id_from_username

# Check if a user is an admin in the current chat
async def is_user_admin(update: Update, user_id: int) -> bool:
    try:
        member = await update.effective_chat.get_member(user_id)
        return member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]
    except:
        return False

# /warn Command
async def warn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_user_admin(update, update.effective_user.id):
        await update.message.reply_text("Only admins can issue warnings.")
        return

    chat_id = update.effective_chat.id
    user = None
    user_id = None

    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        user_id = user.id
    elif context.args:
        arg = context.args[0]
        if arg.isdigit():
            user_id = int(arg)
        elif arg.startswith("@"):
            user_id = await get_user_id_from_username(arg)
            if not user_id:
                await update.message.reply_text("User not found in database.")
                return
        else:
            await update.message.reply_text("Invalid argument. Use /warn @username or user_id.")
            return
    else:
        await update.message.reply_text("Reply to a user or use /warn @username or user_id.")
        return

    # Prevent warning the bot itself
    if user_id == context.bot.id:
        await update.message.reply_text("I can't warn myself 😅")
        return

    # Prevent banning admins
    if await is_user_admin(update, user_id):
        await update.message.reply_text("You can't warn or ban another admin.")
        return

    warn_count = add_warn(user_id, chat_id)

    if warn_count >= 3:
        await context.bot.ban_chat_member(chat_id, user_id)
        reset_warns(user_id, chat_id)
        await update.message.reply_text(
            f"<b>User ID:</b> <code>{user_id}</code> was banned after 3 warnings!",
            parse_mode='HTML'
        )
    else:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Remove Warn ❌", callback_data=f"remove_warn:{user_id}")]
        ])
        await update.message.reply_text(
            f"⚠️ Warning {warn_count}/3 issued to <b>User ID:</b> <code>{user_id}</code>",
            parse_mode='HTML',
            reply_markup=keyboard
        )

# /unwarn Command
async def unwarn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_user_admin(update, update.effective_user.id):
        await update.message.reply_text("Only admins can remove warnings.")
        return

    chat_id = update.effective_chat.id
    user = None
    user_id = None

    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        user_id = user.id
    elif context.args:
        arg = context.args[0]
        if arg.isdigit():
            user_id = int(arg)
        elif arg.startswith("@"):
            db_user = await get_user_from_db(arg[1:])
            if not db_user:
                await update.message.reply_text("User not found in database.")
                return
            user_id = db_user["user_id"]
        else:
            await update.message.reply_text("Invalid argument. Use /unwarn @username or user_id.")
            return
    else:
        await update.message.reply_text("Reply to a user or use /unwarn @username or user_id.")
        return

    new_count = remove_warn(user_id, chat_id)

    await update.message.reply_text(
        f"✅ One warning removed. Current warning count for <b>User ID:</b> <code>{user_id}</code>: {new_count}/3",
        parse_mode='HTML'
    )

# Inline "Remove Warn" button handler
async def handle_remove_warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id
    user_id = int(query.data.split(":")[1])

    if not await is_user_admin(update, query.from_user.id):
        await query.edit_message_text("Only admins can remove warnings.")
        return

    new_count = remove_warn(user_id, chat_id)

    await query.edit_message_text(
        f"✅ One warning removed. Current warning count: {new_count}/3"
    )

# Register handlers
def warn_handlers():
    return [
        CommandHandler("warn", warn_user),
        CommandHandler("unwarn", unwarn_user),
        CallbackQueryHandler(handle_remove_warn, pattern=r"^remove_warn:\d+$")
    ]