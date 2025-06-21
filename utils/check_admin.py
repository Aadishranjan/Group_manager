from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes

def check_admin(permission: str = None, is_both: bool = False):
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            try:
                user_id = update.effective_user.id
                chat_id = update.effective_chat.id

                # Get the member's role in the group
                member = await context.bot.get_chat_member(chat_id, user_id)

                # Allow owner
                if member.status == "creator":
                    return await func(update, context, *args, **kwargs)

                # Check if admin and has required permission
                if member.status == "administrator":
                    if not permission:
                        return await func(update, context, *args, **kwargs)

                    allowed = getattr(member, permission, False)
                    if allowed or is_both:
                        return await func(update, context, *args, **kwargs)

                await update.message.reply_text("❌ You don't have permission to use this command.")
            except Exception as e:
                print(f"[check_admin] Exception: {e}")
                await update.message.reply_text("⚠️ Error checking admin rights.")
        return wrapper
    return decorator