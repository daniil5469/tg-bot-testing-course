import os
import httpx

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")

def send_message(chat_id: int, text: str):
    url = f"{BASE_URL}/bot{BOT_TOKEN}/sendMessage"
    response = httpx.post(url, json={"chat_id": chat_id, "text": text})
    return response
