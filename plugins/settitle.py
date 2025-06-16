from telegram import Update
from telegram.ext import ContextTypes
from utils.user_id import get_user_id_from_username  # your DB lookup

async def set_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    invoker = update.effective_user

    # Check permission of invoker
    invoker_member = await context.bot.get_chat_member(chat_id, invoker.id)
    if invoker_member.status != "creator" and not getattr(invoker_member, "can_promote_members", False):
        await update.message.reply_text("❌ You don't have permission to set admin titles.")
        return

    # Parse target
    if not update.message.reply_to_message and not context.args:
        await update.message.reply_text("❌ Usage: reply to user or /settitle @username Title")
        return

    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
        user_id = target.id
        target_name = target.full_name
        title = " ".join(context.args)
    else:
        arg = context.args[0].lstrip("@")
        if arg.isdigit():
            user_id = int(arg)
            target_name = f"`{user_id}`"
            title = " ".join(context.args[1:])
        else:
            user_id = await get_user_id_from_username(arg)
            if not user_id:
                await update.message.reply_text("❌ User not found in database.")
                return
            target_name = f"@{arg}"
            title = " ".join(context.args[1:])

    if not title.strip():
        await update.message.reply_text("❌ Please provide a title.")
        return

    # Check if target is admin
    try:
        member = await context.bot.get_chat_member(chat_id, user_id)
        if member.status != "administrator":
            await update.message.reply_text("❌ User is not an admin.")
            return
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error checking admin: {e}")
        return

    # Set the admin title using correct method
    try:
        await context.bot.set_chat_administrator_custom_title(
            chat_id=chat_id,
            user_id=user_id,
            custom_title=title
        )
        await update.message.reply_text(
            f"Set title of {target_name} to <b>{title}</b>", parse_mode="HTML"
        )
    except Exception as e:
        await update.message.reply_text(f"⚠️ Failed to set title: {e}")