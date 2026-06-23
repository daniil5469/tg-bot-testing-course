import pytest
from telethon import TelegramClient
import os
from utils.helpers import click_and_refresh, send_and_get_response

API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")
BOT_USERNAME = os.getenv("TG_BOT_USERNAME")
SESSION_NAME = "user_session"

EXPECTED_MENU_BUTTONS = [
    "Create Profile",
    "View Profile",
    "Crypto Market",
    "Delete Profile",
    "Help",
]

EXPECTED_MENU_TEXT_LINES = [
    "Hello! Welcome to Testronaut Bot.",
    "Choose an option to get started:",
]


def assert_main_menu(msg):
    for line in EXPECTED_MENU_TEXT_LINES:
        assert line in msg.text, f"Main menu missing expected text: {line!r}"
    button_texts = [btn.text for row in msg.buttons for btn in row]
    for label in EXPECTED_MENU_BUTTONS:
        assert label in button_texts, f"Main menu missing button: {label!r}"


@pytest.mark.asyncio
async def test_start_shows_main_menu(tg_api_id, tg_api_hash, tg_bot_username):
    async with TelegramClient(SESSION_NAME, tg_api_id, tg_api_hash) as client:
        async with client.conversation(tg_bot_username) as conv:
            await conv.send_message("/start")
            msg = await conv.get_response()

            assert_main_menu(msg)


@pytest.mark.asyncio
async def test_help_button_shows_help_text(tg_api_id, tg_api_hash, tg_bot_username):
    async with TelegramClient(SESSION_NAME, tg_api_id, tg_api_hash) as client:
        async with client.conversation(tg_bot_username) as conv:
            await conv.send_message("/start")
            msg = await conv.get_response()

            msg = await click_and_refresh(msg, client, "Help")

            assert "/start" in msg.text
            assert "Back to Main Menu" in [btn.text for row in msg.buttons for btn in row]


@pytest.mark.asyncio
async def test_back_to_main_menu_from_help(tg_api_id, tg_api_hash, tg_bot_username):
    async with TelegramClient(SESSION_NAME, tg_api_id, tg_api_hash) as client:
        async with client.conversation(tg_bot_username) as conv:
            await conv.send_message("/start")
            msg = await conv.get_response()

            msg = await click_and_refresh(msg, client, "Help")
            msg = await click_and_refresh(msg, client, "Back to Main Menu")

            assert_main_menu(msg)


@pytest.mark.asyncio
async def test_view_profile_button_responds(tg_api_id, tg_api_hash, tg_bot_username):
    async with TelegramClient(SESSION_NAME, tg_api_id, tg_api_hash) as client:
        async with client.conversation(tg_bot_username) as conv:
            await conv.send_message("/start")
            msg = await conv.get_response()

            msg = await click_and_refresh(msg, client, "View Profile")

            assert msg.text is not None
            assert len(msg.text.strip()) > 0


@pytest.mark.asyncio
async def test_back_to_main_menu_from_view_profile(tg_api_id, tg_api_hash, tg_bot_username):
    async with TelegramClient(SESSION_NAME, tg_api_id, tg_api_hash) as client:
        async with client.conversation(tg_bot_username) as conv:
            await conv.send_message("/start")
            msg = await conv.get_response()

            msg = await click_and_refresh(msg, client, "View Profile")
            msg = await click_and_refresh(msg, client, "Back to Main Menu")

            assert_main_menu(msg)


@pytest.mark.asyncio
async def test_crypto_market_button_opens_crypto_menu(tg_api_id, tg_api_hash, tg_bot_username):
    async with TelegramClient(SESSION_NAME, tg_api_id, tg_api_hash) as client:
        async with client.conversation(tg_bot_username) as conv:
            await conv.send_message("/start")
            msg = await conv.get_response()

            msg = await click_and_refresh(msg, client, "Crypto Market")

            assert "Crypto Market:" in msg.text
            button_texts = [btn.text for row in msg.buttons for btn in row]
            assert "Back to Main Menu" in button_texts


@pytest.mark.asyncio
async def test_back_to_main_menu_from_crypto(tg_api_id, tg_api_hash, tg_bot_username):
    async with TelegramClient(SESSION_NAME, tg_api_id, tg_api_hash) as client:
        async with client.conversation(tg_bot_username) as conv:
            await conv.send_message("/start")
            msg = await conv.get_response()

            msg = await click_and_refresh(msg, client, "Crypto Market")
            msg = await click_and_refresh(msg, client, "Back to Main Menu")

            assert_main_menu(msg)
