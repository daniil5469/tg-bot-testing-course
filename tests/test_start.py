import os
import time
from utils.helpers import send_message

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

def test_start_command_trigger():
    print("📤 Sending `/start` to bot...")
    resp = send_message(CHAT_ID, "/start")
    assert resp.status_code == 200, f"Failed to send /start: {resp.text}"
    print("✅ /start sent successfully.")

    print("👀 Please check your Telegram — did the bot reply?")
    time.sleep(5)  # Give bot time to respond (or log output)
