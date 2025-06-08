import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PUBLIC_URL = os.getenv("PUBLIC_URL")
BASE_URL = os.getenv("BASE_URL")

if TELEGRAM_BOT_TOKEN is None:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in .env file.")

if PUBLIC_URL is None:
    raise ValueError("PUBLIC_URL not found in .env file.")

if BASE_URL is None:
    raise ValueError("BASE_URL nor found in the .env file.")