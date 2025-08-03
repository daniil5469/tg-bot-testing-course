from telethon import TelegramClient
import os

API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")
PHONE = os.getenv("TG_PHONE")
SESSION_NAME = "test_session"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
