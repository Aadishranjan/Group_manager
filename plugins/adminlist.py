from telegram import Update
from telegram.ext import ContextTypes

async def admin_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    try:
        admins = await context.bot.get_chat_administrators(chat.id)

        owner = None
        other_admins = []

        for admin in admins:
            user = admin.user
            if admin.status == "creator":
                owner = user
            else:
                other_admins.append(user)

        text = "👑 <b>Owner</b>\n"
        if owner:
            username = f"@{owner.username}" if owner.username else owner.full_name
            text += f" └─ {username}\n"

        text += "\n🛡️ <b>Admins</b>\n"
        if other_admins:
            for i, user in enumerate(other_admins):
                username = f"@{user.username}" if user.username else user.full_name
                prefix = " └─" if i == len(other_admins) - 1 else " ├─"
                text += f"{prefix} {username}\n"
        else:
            text += " └─ No other admins found.\n"

        await update.message.reply_text(text, parse_mode="HTML")
    
    except Exception as e:
        await update.message.reply_text(f"⚠️ Failed to fetch admin list:\n<code>{e}</code>", parse_mode="HTML")