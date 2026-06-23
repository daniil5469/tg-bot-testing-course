import asyncio
import re
import pytest
from telethon import TelegramClient
import os
from utils.helpers import click_and_refresh

API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")
BOT_USERNAME = os.getenv("TG_BOT_USERNAME")
SESSION_NAME = "user_session"

CRYPTO_LINE_REGEX = re.compile(
    r"""
    ^[⭐☆]\s                # star icon
    .+\s\([A-Z0-9]+\):\s    # coin name + ticker
    \$[\d,]+(\.\d{1,2})?\s  # price (may include commas)
    [+-]\d+(\.\d{1,2})?%$   # 24h percentage change
    """,
    re.VERBOSE,
)


def assert_crypto_market_message(text: str, expected_coins: list[str]):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    assert lines[0] == "Crypto Market:", "Missing 'Crypto Market:' header"
    for coin in expected_coins:
        assert any(coin in line for line in lines), f"{coin} not found in crypto market message"
    for line in lines[1:]:
        assert CRYPTO_LINE_REGEX.match(line), f"Unexpected line format: {line!r}"


@pytest.mark.asyncio
async def test_crypto_market_message(tg_api_id, tg_api_hash, tg_bot_username, expected_crypto_coins):
    async with TelegramClient(SESSION_NAME, tg_api_id, tg_api_hash) as client:
        async with client.conversation(tg_bot_username) as conv:
            await conv.send_message("/start")
            msg = await conv.get_response()

            msg = await click_and_refresh(msg, client, "Crypto Market")

            assert_crypto_market_message(msg.text, expected_crypto_coins)


@pytest.mark.asyncio
async def test_favorites_tab_is_empty_for_new_user(tg_api_id, tg_api_hash, tg_bot_username):
    async with TelegramClient(SESSION_NAME, tg_api_id, tg_api_hash) as client:
        async with client.conversation(tg_bot_username) as conv:
            await conv.send_message("/start")
            msg = await conv.get_response()

            msg = await click_and_refresh(msg, client, "Crypto Market")
            msg = await click_and_refresh(msg, client, "Favorites")

            assert "no favorite" in msg.text.lower() or "Your Favorite Coins:" in msg.text


@pytest.mark.asyncio
async def test_toggle_coin_adds_to_favorites(tg_api_id, tg_api_hash, tg_bot_username):
    async with TelegramClient(SESSION_NAME, tg_api_id, tg_api_hash) as client:
        async with client.conversation(tg_bot_username) as conv:
            await conv.send_message("/start")
            msg = await conv.get_response()

            msg = await click_and_refresh(msg, client, "Crypto Market")
            stars_before = msg.text.count("⭐")

            # Toggle Bitcoin favorite using its known callback data
            await msg.click(data=b"toggle_fav_bitcoin")
            await asyncio.sleep(1)
            msg = await client.get_messages(msg.peer_id, ids=msg.id)

            stars_after = msg.text.count("⭐")
            assert stars_after == stars_before + 1, (
                f"Expected {stars_before + 1} starred coins, got {stars_after}"
            )

            # Cleanup: toggle back off
            await msg.click(data=b"toggle_fav_bitcoin")
            await asyncio.sleep(1)


@pytest.mark.asyncio
async def test_favorited_coin_appears_in_favorites_tab(tg_api_id, tg_api_hash, tg_bot_username):
    async with TelegramClient(SESSION_NAME, tg_api_id, tg_api_hash) as client:
        async with client.conversation(tg_bot_username) as conv:
            await conv.send_message("/start")
            msg = await conv.get_response()

            msg = await click_and_refresh(msg, client, "Crypto Market")

            # Add Bitcoin to favorites
            await msg.click(data=b"toggle_fav_bitcoin")
            await asyncio.sleep(1)
            msg = await client.get_messages(msg.peer_id, ids=msg.id)

            # Switch to Favorites tab
            msg = await click_and_refresh(msg, client, "Favorites")
            assert "Bitcoin" in msg.text, "Favorited coin 'Bitcoin' not shown in Favorites tab"

            # Cleanup: go back to market and remove favorite
            msg = await click_and_refresh(msg, client, "Back to Market")
            await msg.click(data=b"toggle_fav_bitcoin")
            await asyncio.sleep(1)
