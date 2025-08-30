from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from utils.user_id import get_user_id_from_username
from utils.check_admin import check_admin


# 🔍 Check if target is admin
async def is_user_admin(update: Update, user_id: int) -> bool:
    try:
        member = await update.effective_chat.get_member(user_id)
        return member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]
    except:
        return False


@check_admin(permission="can_restrict_members")
async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    args = context.args

    # 🔹 Determine target user
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        user_id = user.id
        target_name = user.mention_html()
    elif args:
        arg = args[0].lstrip("@")
        if arg.isdigit():
            user_id = int(arg)
            target_name = f"<code>{user_id}</code>"
        else:
            user_id = await get_user_id_from_username(arg)
            if not user_id:
                await update.message.reply_text("❌ User not found in database.")
                return
            target_name = f"@{arg}"
    else:
        await update.message.reply_text("❌ Usage: reply to a user or use /kick @username or /kick <user_id>")
        return

    # 🔐 Prevent kicking other admins
    if await is_user_admin(update, user_id):
        await update.message.reply_text("⚠️ Why would I kick an admin? That sound like pretty dumb idea.")
        return

    # 🚫 Kick user
    try:
        await context.bot.ban_chat_member(chat_id, user_id)
        await context.bot.unban_chat_member(chat_id, user_id)  # Optional: allows them to rejoin
        await update.message.reply_html(f"✅ Kicked {target_name} from the group.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Failed to kick: {e}")
