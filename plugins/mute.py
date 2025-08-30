from telegram import Update, ChatPermissions, ChatMember
from telegram.ext import ContextTypes
from utils.user_id import get_user_id_from_username

MUTE_PERMISSIONS = ChatPermissions(can_send_messages=False)
UNMUTE_PERMISSIONS = ChatPermissions(can_send_messages=True)


# 🔍 Check if user is admin
async def is_user_admin(update: Update, user_id: int) -> bool:
    try:
        member = await update.effective_chat.get_member(user_id)
        return member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]
    except:
        return False


# 🔹 Extract user from reply, @username, or ID
async def extract_target_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = None
    user_id = None

    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        return user, user.id

    elif context.args:
        arg = context.args[0]
        if arg.isdigit():
            return None, int(arg)
        elif arg.startswith("@"):
            user_id = await get_user_id_from_username(arg)
            if user_id:
                return None, user_id
            else:
                await update.message.reply_text("❌ User not found in database.")
                return None, None
        else:
            await update.message.reply_text("❌ Invalid argument. Use reply, @username, or user_id.")
            return None, None
    else:
        await update.message.reply_text("⚠️ Please reply to a user or use /command @username or user_id.")
        return None, None


# 🔇 Mute command
async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_user_admin(update, update.effective_user.id):
        await update.message.reply_text("❌ You must be an admin to use this command.")
        return

    user, user_id = await extract_target_user(update, context)
    if not user_id:
        return

    if await is_user_admin(update, user_id):
        await update.message.reply_text("⚠️ Why would I mute an admin? That sound like pretty dumb idea.")
        return

    try:
        await context.bot.restrict_chat_member(update.effective_chat.id, user_id, permissions=MUTE_PERMISSIONS)
        await update.message.reply_text(f"🔇 Muted <code>{user_id}</code>", parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to mute: {e}")


# 🔊 Unmute command
async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_user_admin(update, update.effective_user.id):
        await update.message.reply_text("❌ You must be an admin to use this command.")
        return

    user, user_id = await extract_target_user(update, context)
    if not user_id:
        return

    if await is_user_admin(update, user_id):
        await update.message.reply_text("⚠️ That user is an admin and shouldn't be unmuted manually.")
        return

    try:
        await context.bot.restrict_chat_member(update.effective_chat.id, user_id, permissions=UNMUTE_PERMISSIONS)
        await update.message.reply_text(f"🔊 Unmuted <code>{user_id}</code>", parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to unmute: {e}")


# 🚫 Ban command
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_user_admin(update, update.effective_user.id):
        await update.message.reply_text("❌ You must be an admin to use this command.")
        return

    user, user_id = await extract_target_user(update, context)
    if not user_id:
        return

    if await is_user_admin(update, user_id):
        await update.message.reply_text("⚠️ Why would I  ban an admin? That sound like pretty dumb idea.")
        return

    try:
        await context.bot.ban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text(f"🚫 Banned <code>{user_id}</code>", parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to ban: {e}")


# ✅ Unban command
async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_user_admin(update, update.effective_user.id):
        await update.message.reply_text("❌ You must be an admin to use this command.")
        return

    user, user_id = await extract_target_user(update, context)
    if not user_id:
        return

    try:
        await context.bot.unban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text(f"✅ Unbanned <code>{user_id}</code>", parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to unban: {e}")
