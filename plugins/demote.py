from telegram import Update, ChatAdministratorRights
from telegram.ext import ContextTypes
from utils.user_id import get_user_id_from_username  # your DB lookup function

async def demote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    invoker = update.effective_user

    # Check if the invoker has rights to demote
    invoker_member = await context.bot.get_chat_member(chat_id, invoker.id)
    if invoker_member.status != "creator" and not getattr(invoker_member, "can_promote_members", False):
        await update.message.reply_text("❌ You don't have permission to demote admins.")
        return

    # Determine the target user
    target_user_id = None
    target_name = None

    # 1. Reply-based demotion
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
        target_user_id = target_user.id
        target_name = target_user.full_name

    # 2. Username or user_id from arguments
    elif context.args:
        arg = context.args[0].lstrip("@")
        if arg.isdigit():
            target_user_id = int(arg)
            target_name = f"`{target_user_id}`"
        else:
            target_user_id = await get_user_id_from_username(arg)
            target_name = f"@{arg}"

        if not target_user_id:
            await update.message.reply_text("❌ User not found in the database.")
            return

    else:
        await update.message.reply_text("❌ Reply to a user or provide @username or user ID.")
        return

    # Define rights to revoke all admin privileges
    revoke_rights = ChatAdministratorRights(
        is_anonymous=False,
        can_manage_chat=False,
        can_change_info=False,
        can_post_messages=False,
        can_edit_messages=False,
        can_delete_messages=False,
        can_invite_users=False,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_video_chats=False
    )

    try:
        await context.bot.promote_chat_member(
            chat_id=chat_id,
            user_id=target_user_id,
            **revoke_rights.to_dict()
        )
        await update.message.reply_text(f"✅ Demoted {target_name} to normal member.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Failed to demote: {e}")