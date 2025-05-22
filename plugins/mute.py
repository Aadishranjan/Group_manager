from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes

# Mute permission: user can't send anything
MUTE_PERMISSIONS = ChatPermissions(can_send_messages=False)

# Unmute permission: user can send messages
UNMUTE_PERMISSIONS = ChatPermissions(can_send_messages=True)

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Tag a user to mute them.")
        return

    user = update.message.reply_to_message.from_user
    try:
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user.id,
            permissions=MUTE_PERMISSIONS
        )
        await update.message.reply_text(f"Muted {user.mention_html()}", parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Failed to mute: {e}")

async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Tag a user to unmute them.")
        return

    user = update.message.reply_to_message.from_user
    try:
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user.id,
            permissions=UNMUTE_PERMISSIONS
        )
        await update.message.reply_text(f"Unmuted {user.mention_html()}", parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Failed to unmute: {e}")

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Tag a user to ban them.")
        return

    user = update.message.reply_to_message.from_user
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, user.id)
        await update.message.reply_text(f"Banned {user.mention_html()}", parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Failed to ban: {e}")

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Tag a user to unban them.")
        return

    user = update.message.reply_to_message.from_user
    try:
        await context.bot.unban_chat_member(update.effective_chat.id, user.id)
        await update.message.reply_text(f"Unbanned {user.mention_html()}", parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Failed to unban: {e}")
