import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from scripts.update_ngrok_env import update_ngrok_env
from scripts.update_webhook import update_telegram_webhook

import logging
import asyncio
import traceback
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from src.handlers import profile, crypto, start
from src.config import TELEGRAM_BOT_TOKEN, CHAT_ID

# Load .env before anything else
load_dotenv()

# Flask app for webhook
app = Flask(__name__)

# Global asyncio loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="bot.log",
)

# Global application object
application: Application = None

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        print("📩 Incoming webhook update:", data)

        update = Update.de_json(data, application.bot)
        asyncio.run_coroutine_threadsafe(application.process_update(update), loop)

    except Exception as e:
        print("❌ Error processing update:", e)
        traceback.print_exc()

    print("✅ Returning 200 OK to Telegram")
    return "ok", 200

async def create_application():
    app_instance = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    if CHAT_ID:
        try:
            await Bot(token=TELEGRAM_BOT_TOKEN).send_message(chat_id=CHAT_ID, text="🤖 Bot ready!")
        except Exception as e:
            print("❌ Failed to send startup message:", e)

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

    # Command handlers
    app_instance.add_handler(CommandHandler("start", start.start))
    app_instance.add_handler(CommandHandler("view_profile", profile.view_profile))
    app_instance.add_handler(CommandHandler("delete_profile", profile.delete_profile))
    app_instance.add_handler(CommandHandler("help", profile.help_command))
    app_instance.add_handler(CommandHandler("crypto", crypto.show_crypto_menu))
    app_instance.add_handler(profile_convo)
    app_instance.add_handler(CallbackQueryHandler(crypto.handle_crypto_callback, pattern=r"^(show_market|show_favorites|toggle_fav_.*)$"))
    app_instance.add_handler(CallbackQueryHandler(profile.button_handler))
    app_instance.add_handler(MessageHandler(filters.COMMAND, profile.unknown_command))

    return app_instance

def run_webhook():
    global application

    from scripts.update_ngrok_env import update_ngrok_env
    from scripts.update_webhook import update_telegram_webhook

    # 🟢 1. Start ngrok and update .env
    public_url = update_ngrok_env()

    # 🟢 2. Register webhook with Telegram
    update_telegram_webhook(public_url)

    # 🟢 3. Обновим переменные окружения для дальнейшего использования
    os.environ["PUBLIC_URL"] = public_url

    # 🟢 4. Init Telegram application
    if not TELEGRAM_BOT_TOKEN or not public_url:
        print("❌ Missing TELEGRAM_BOT_TOKEN or PUBLIC_URL")
        return

    application = asyncio.run(create_application())

    # 🟢 5. Run Flask app
    print(f"🌐 Webhook mode: listening on {public_url}/webhook")
    app.run(host="0.0.0.0", port=8443, debug=True)

def run_bot():
    global application
    application = asyncio.run(create_application())
    print("🤖 Polling mode started")
    application.run_polling()
