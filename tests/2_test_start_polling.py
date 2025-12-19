import pytest
import asyncio
from telethon import TelegramClient
import os

EXPECTED_LINES = [
    "Hello! Welcome to Testronaut Bot.",
    "Choose an option to get started:"
]

@pytest.mark.asyncio
async def test_start_command_reply_polling(tg_api_id, tg_api_hash, tg_bot_username):
    """
    Verify /start command sends greeting message in polling mode.
    """
    SESSION_NAME = os.getenv("SESSION_NAME", "user_session")

    async with TelegramClient(SESSION_NAME, tg_api_id, tg_api_hash) as client:
        # Send /start to the bot
        await client.send_message(tg_bot_username, "/start")

        start_time = asyncio.get_event_loop().time()

        while asyncio.get_event_loop().time() - start_time < 5:
            messages = await client.get_messages(tg_bot_username, limit=5)

            for msg in messages:
                if not msg.text:
                    continue

                text = msg.text.strip()

                if all(line in text for line in EXPECTED_LINES):
                    return  # Success

            await asyncio.sleep(0.5)

        raise AssertionError(
            f"Expected greeting not found. Last messages: {[m.text for m in messages if m.text]}"
        )
