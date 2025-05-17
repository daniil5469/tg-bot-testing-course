from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN, CHAT_ID
from handlers import profile, crypto, start
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

def run_bot():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    if CHAT_ID:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        try:
            bot.send_message(chat_id=CHAT_ID, text="✅ Bot has started and is ready!")
        except Exception as e:
            print(f"⚠️ Failed to send test message to CHAT_ID: {e}")

    # Profile creation/editing conversation handler
    profile_convo = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                profile.button_handler,
                pattern="^create_profile$",
            )
        ],
        states={
            profile.NICKNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, profile.get_nickname)],
            profile.EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, profile.get_email)],
            profile.DOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, profile.get_dob)],
            profile.LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, profile.get_location)],
        },
        fallbacks=[CommandHandler("cancel", profile.cancel)],
        allow_reentry=True,
    )

    # Register command handlers for profile
    application.add_handler(CommandHandler("start", start.start))
    application.add_handler(CommandHandler("view_profile", profile.view_profile))
    application.add_handler(CommandHandler("help", profile.help_command))
    application.add_handler(CommandHandler("delete_profile", profile.delete_profile))

    # Add profile conversation handler
    application.add_handler(profile_convo)

    # Register /crypto command to open the crypto menu
    application.add_handler(CommandHandler("crypto", crypto.show_crypto_menu))

    # Register callback query handler for all crypto inline button callbacks
    application.add_handler(
        CallbackQueryHandler(
            crypto.handle_crypto_callback,
            pattern=r"^(show_market|show_favorites|toggle_fav_.*)$"
        )
    )

    # Generic callback query handler for other profile inline buttons
    application.add_handler(CallbackQueryHandler(profile.button_handler))

    # Unknown commands handler
    application.add_handler(MessageHandler(filters.COMMAND, profile.unknown_command))

    print("🚀 Bot is polling. Press Ctrl+C to stop.")
    application.run_polling()
