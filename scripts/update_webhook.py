import os
import requests
import time
from dotenv import load_dotenv
import sys

# Allow import from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import TELEGRAM_BOT_TOKEN


def update_telegram_webhook(public_url):
    load_dotenv()
    url = f"{public_url}/webhook"
    
    if not TELEGRAM_BOT_TOKEN or not public_url:
        raise ValueError("Missing TELEGRAM_BOT_TOKEN or PUBLIC_URL")

    # Delete old webhook (to avoid 429 errors)
    print("Deleting old webhook (if any)...")
    delete_response = requests.post(
    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook",
    json={"drop_pending_updates": True}
    )
    if delete_response.ok:
        print("Old webhook deleted.")
    else:
        print("Failed to delete webhook:", delete_response.text)

    # Short delay to avoid "Too Many Requests"
    time.sleep(1)

    # Set new webhook
    print(f"Setting new webhook to {url}...")
    set_response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook",
        json={"url": url}
    )
    if set_response.ok and set_response.json().get("ok"):
        print(f"Webhook set successfully to {url}")
    else:
        print("❌ Failed to set webhook:", set_response.text)
