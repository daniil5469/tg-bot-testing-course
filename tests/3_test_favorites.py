import os
import re
import json
import pytest
from telethon import TelegramClient
from utils.helpers import click_and_refresh, send_and_get_response

API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")
BOT_USERNAME = os.getenv("TG_BOT_USERNAME")
PHONE = os.getenv("TG_PHONE")
SESSION_NAME = "user_session"

# Regex for top-listed crypto coins
CRYPTO_LINE_REGEX = re.compile(
    r"""
    ^[⭐☆]\s                # star icon
    .+\s\([A-Z0-9]+\):\s    # coin name + ticker
    \$\d+(\.\d{1,2})?\s     # price
    [+-]\d+(\.\d{1,2})?%$   # percentage change
    """,
    re.VERBOSE
)

# Assertion helper to verify message
def assert_crypto_market_message(text: str, expected_coins: list[str]):
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    assert lines[0] == "Crypto Market:", "Missing header"

    for coin in expected_coins:
        assert any(coin in line for line in lines), f"{coin} not found in message"

    for line in lines[1:]:
        assert CRYPTO_LINE_REGEX.match(line), f"Invalid crypto line format: {line}"

@pytest.mark.asyncio
async def test_crypto_market_message(
    tg_api_id,
    tg_api_hash,
    tg_bot_username,
    expected_crypto_coins
):
    async with TelegramClient("user_session", tg_api_id, tg_api_hash) as client:
        async with client.conversation(tg_bot_username) as conv:
            await conv.send_message("/start")
            msg = await conv.get_response()

            msg = await click_and_refresh(msg, client, "Crypto Market")

            assert_crypto_market_message(msg.text, expected_crypto_coins)

@pytest.mark.asyncio
async def test_profile_creation_and_viewing(test_profile_data, expected_profile_text):
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        async with client.conversation(BOT_USERNAME) as conv:
            # Start bot
            await conv.send_message("/start")
            msg = await conv.get_response()

            # View profile (should be empty)
            msg = await click_and_refresh(msg, client, "Crypto")
            assert "Profile not found" in msg.text

            # Back to main menu
            msg = await click_and_refresh(msg, client, "Back to Main Menu")

            # Start profile creation
            msg = await click_and_refresh(msg, client, "Create Profile")
            assert "Please enter your nickname" in msg.text

            # Send nickname
            msg = await send_and_get_response(conv, test_profile_data["nickname"])
            assert "Please enter your email address" in msg.text

            # Send email
            msg = await send_and_get_response(conv, test_profile_data["email"])
            assert "Please enter your date of birth" in msg.text

            # Send DOB
            msg = await send_and_get_response(conv, test_profile_data["dob"])
            assert "Please enter your location" in msg.text

            # Send location
            msg = await send_and_get_response(conv, test_profile_data["location"])
            assert "Profile created successfully!" in msg.text

            # View Profile again
            msg = await click_and_refresh(msg, client, "View Profile")
            assert expected_profile_text in msg.text.strip()

            # Back to main menu
            msg = await click_and_refresh(msg, client, "Back to Main Menu")

            # Delete created profile
            msg = await click_and_refresh(msg, client, "Delete Profile")
            assert "Your profile has been deleted successfully." in msg.text

            # Back to main menu
            msg = await click_and_refresh(msg, client, "Back to Main Menu")
            assert "Welcome back! Please choose an option:" in msg.text