import asyncio
import logging
import requests
import os
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from src.handlers import profile, crypto, start
from src.config import TELEGRAM_BOT_TOKEN, CHAT_ID

# Global instances
app = Flask(__name__)
application = None  # Initialized later

# Logging setup
logging.basicConfig(
    filename="bot.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

@app.route("/webhook", methods=["POST"])
def webhook():
    global application
    print("Incoming webhook hit!")

    if application is None:
        print("Application not initialized, creating now.")
        application = asyncio.run(create_application())

    try:
        data = request.get_json(force=True)
        print("Raw update:", data)
        update = Update.de_json(data, application.bot)
        asyncio.run(application.process_update(update))
    except Exception as e:
        print("Error processing update:", e)

    return "ok", 200

async def create_application():
    app_instance = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Initialize the app before returning
    await app_instance.initialize()

    # Optional startup message
    if CHAT_ID:
        try:
            Bot(token=TELEGRAM_BOT_TOKEN).send_message(chat_id=CHAT_ID, text="Bot has started and is ready!")
        except Exception as e:
            print(f"Failed to send test message: {e}")

    # Profile conversation
    profile_convo = ConversationHandler(
        entry_points=[CallbackQueryHandler(profile.button_handler, pattern="^create_profile$")],
        states={
            profile.NICKNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, profile.get_nickname)],
            profile.EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, profile.get_email)],
            profile.DOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, profile.get_dob)],
            profile.LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, profile.get_location)],
        },
        fallbacks=[CommandHandler("cancel", profile.cancel)],
        allow_reentry=True,
    )

    # Register handlers
    app_instance.add_handler(CommandHandler("start", start.start))
    app_instance.add_handler(CommandHandler("view_profile", profile.view_profile))
    app_instance.add_handler(CommandHandler("help", profile.help_command))
    app_instance.add_handler(CommandHandler("delete_profile", profile.delete_profile))
    app_instance.add_handler(CommandHandler("crypto", crypto.show_crypto_menu))
    app_instance.add_handler(profile_convo)
    app_instance.add_handler(CallbackQueryHandler(crypto.handle_crypto_callback, pattern=r"^(show_market|show_favorites|toggle_fav_.*)$"))
    app_instance.add_handler(CallbackQueryHandler(profile.button_handler))
    app_instance.add_handler(MessageHandler(filters.COMMAND, profile.unknown_command))

    return app_instance

def run_bot():
    global application
    application = asyncio.run(create_application())
    print("🤖 Bot is running in polling mode...")
    application.run_polling()

def run_webhook():
    # Load updated environment variables
    load_dotenv()
    public_url = os.getenv("PUBLIC_URL")
    webhook_path = "/webhook"
    full_webhook_url = f"{public_url}{webhook_path}"

    if not TELEGRAM_BOT_TOKEN or not public_url:
        print("TELEGRAM_BOT_TOKEN or PUBLIC_URL is missing in .env")
        return

    # Create Telegram bot application
    global application
    application = asyncio.run(create_application())

    # Set Telegram webhook
    telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"
    try:
        response = requests.post(telegram_api_url, json={"url": full_webhook_url})
        response_data = response.json()
        if response.ok and response_data.get("ok"):
            print(f"Webhook set successfully to {full_webhook_url}")
        else:
            print(f"Failed to set webhook: {response_data}")
    except Exception as e:
        print(f"Exception while setting webhook: {e}")
        return

    print(f"Webhook mode: listening on {full_webhook_url}")

    # Start Flask server
    app.run(host="0.0.0.0", port=8443)