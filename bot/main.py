import asyncio
import logging
import sys
from pathlib import Path

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
)

sys.path.append(str(Path(__file__).parent.parent))

from core.config import settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

LANGUAGE_SELECTION = 0

MESSAGES = {
    "fa": {
        "welcome": "👋 به **SprachSchmiedeBot** خوش آمدید!\n\nکارگاه زبان آلمانی شما",
        "success": "✅ زبان با موفقیت به **فارسی** تنظیم شد.",
    },
    "en": {
        "welcome": "👋 Welcome to **SprachSchmiedeBot**!\n\nYour German Language Forge",
        "success": "✅ Language has been set to **English**.",
    },
    "de": {
        "welcome": "👋 Willkommen bei **SprachSchmiedeBot**!\n\nIhre deutsche Sprachschmiede",
        "success": "✅ Sprache wurde auf **Deutsch** eingestellt.",
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command with clean language selection"""
    keyboard = [
        [
            InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        ],
        [InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de")]
    ]

    welcome_text = (
        "🌟 **SprachSchmiedeBot** 🌟\n\n"
        "به کارگاه زبان آلمانی خوش آمدید\n"
        "Welcome to the German Language Forge\n"
        "Willkommen in der deutschen Sprachschmiede\n\n"
        "لطفاً زبان رابط را انتخاب کنید:\n"
        "Please choose your interface language:\n"
        "Bitte wählen Sie Ihre Sprache:"
    )

    await update.message.reply_text(
        text=welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    return LANGUAGE_SELECTION


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    lang_code = query.data.split("_")[1]
    context.user_data["preferred_language"] = lang_code
    
    msg = MESSAGES[lang_code]
    
    await query.edit_message_text(
        text=f"{msg['welcome']}\n\n{msg['success']}\n\n"
             "📚 منوی اصلی به زودی اضافه خواهد شد.",
        parse_mode="Markdown"
    )
    return ConversationHandler.END


def main():
    if not settings.BOT_TOKEN or "your_bot_token" in settings.BOT_TOKEN.lower():
        logger.error("❌ BOT_TOKEN در فایل .env تنظیم نشده است!")
        return

    app = Application.builder().token(settings.BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE_SELECTION: [CallbackQueryHandler(language_callback, pattern="^lang_")]
        },
        fallbacks=[CommandHandler("start", start)],
        per_message=False,
    )

    app.add_handler(conv_handler)

    print("🚀 SprachSchmiedeBot is running... (Ctrl+C to stop)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    asyncio.run(main())
