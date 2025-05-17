from core.dispatcher import run_bot
from telegram.ext import CommandHandler, CallbackQueryHandler 
from handlers import crypto

if __name__ == "__main__":
    run_bot()
