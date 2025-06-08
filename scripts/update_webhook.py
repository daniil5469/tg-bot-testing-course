# scripts/update_webhook.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PUBLIC_URL = os.getenv("PUBLIC_URL")

def set_telegram_webhook(public_url=None):
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("Missing TELEGRAM_BOT_TOKEN in environment")
    
    if not public_url:
        public_url = PUBLIC_URL
    if not public_url:
        raise ValueError("Missing PUBLIC_URL in environment")

    webhook_url = f"{public_url}/webhook"
    telegram_api = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"

    try:
        response = requests.post(telegram_api, json={"url": webhook_url})
        data = response.json()
        if data.get("ok"):
            print(f"Webhook set to {webhook_url}")
        else:
            print(f"Webhook error: {data}")
    except Exception as e:
        print(f"Failed to set webhook: {e}")
