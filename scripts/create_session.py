"""
Run this script once to create user_session.session for Telethon E2E tests.
It authenticates as a real Telegram user (not a bot) using your phone number.

Usage:
    python scripts/create_session.py
"""

import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")
PHONE = os.getenv("TG_PHONE")
SESSION_NAME = os.getenv("SESSION_NAME", "user_session")


async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start(phone=PHONE)
    me = await client.get_me()
    print(f"Logged in as: {me.first_name} (@{me.username})")
    print(f"Session saved to: {SESSION_NAME}.session")
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
