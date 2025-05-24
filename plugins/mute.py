from telegram import Update, ChatPermissions, ChatMember
from telegram.ext import ContextTypes

MUTE_PERMISSIONS = ChatPermissions(can_send_messages=False)
UNMUTE_PERMISSIONS = ChatPermissions(can_send_messages=True)

async def is_user_admin(update: Update, user_id: int) -> bool:
    try:
        chat_member = await update.effective_chat.get_member(user_id)
        return chat_member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]
    except Exception:
        return False

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_user_admin(update, update.effective_user.id):
        await update.message.reply_text("You must be an admin to use this command.")
        return

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
    if not await is_user_admin(update, update.effective_user.id):
        await update.message.reply_text("You must be an admin to use this command.")
        return

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
    if not await is_user_admin(update, update.effective_user.id):
        await update.message.reply_text("You must be an admin to use this command.")
        return

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
    if not await is_user_admin(update, update.effective_user.id):
        await update.message.reply_text("You must be an admin to use this command.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Tag a user to unban them.")
        return

    user = update.message.reply_to_message.from_user
    try:
        await context.bot.unban_chat_member(update.effective_chat.id, user.id)
        await update.message.reply_text(f"Unbanned {user.mention_html()}", parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Failed to unban: {e}")
