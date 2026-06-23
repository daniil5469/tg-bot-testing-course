import pytest
from faker import Faker
from telethon import TelegramClient
import os
from src.services.user_store import get_user, delete_user_profile, save_user
from utils.helpers import click_and_refresh, send_and_get_response

API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")
BOT_USERNAME = os.getenv("TG_BOT_USERNAME")
SESSION_NAME = "user_session"

fake = Faker()

# ---------------------------------------------------------------------------
# Unit: user_store edge cases (no bot required)
# ---------------------------------------------------------------------------

def test_get_user_returns_none_for_nonexistent_user():
    assert get_user(0) is None


def test_delete_nonexistent_user_returns_false():
    assert delete_user_profile(0) is False


def test_get_user_after_delete_returns_none():
    chat_id = 88887777
    save_user(chat_id, {"nickname": "temp", "email": "t@t.com", "dob": "2000-01-01", "location": "X"})
    delete_user_profile(chat_id)
    assert get_user(chat_id) is None


# ---------------------------------------------------------------------------
# E2E: invalid inputs during profile creation (bot required)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_invalid_nickname_is_rejected(tg_api_id, tg_api_hash, tg_bot_username):
    async with TelegramClient(SESSION_NAME, tg_api_id, tg_api_hash) as client:
        async with client.conversation(tg_bot_username, timeout=15) as conv:
            await conv.send_message("/start")
            msg = await conv.get_response()

            msg = await click_and_refresh(msg, client, "Create Profile")
            assert "nickname" in msg.text.lower()

            # Send nickname with spaces — should be rejected
            msg = await send_and_get_response(conv, "invalid nickname")
            assert "invalid" in msg.text.lower() or "only letters" in msg.text.lower()

            # Recover: send valid nickname to exit conversation cleanly
            msg = await send_and_get_response(conv, fake.user_name())
            msg = await send_and_get_response(conv, fake.email())
            msg = await send_and_get_response(conv, "01/01/1990")
            msg = await send_and_get_response(conv, fake.city())

            # Cleanup: delete the profile just created
            msg = await click_and_refresh(msg, client, "Delete Profile")
            assert "deleted" in msg.text.lower()


@pytest.mark.asyncio
async def test_invalid_email_is_rejected(tg_api_id, tg_api_hash, tg_bot_username):
    async with TelegramClient(SESSION_NAME, tg_api_id, tg_api_hash) as client:
        async with client.conversation(tg_bot_username, timeout=15) as conv:
            await conv.send_message("/start")
            msg = await conv.get_response()

            msg = await click_and_refresh(msg, client, "Create Profile")
            msg = await send_and_get_response(conv, fake.user_name())

            # Send malformed email — should be rejected
            msg = await send_and_get_response(conv, "not-an-email")
            assert "invalid" in msg.text.lower() or "email" in msg.text.lower()

            # Recover: provide valid email and complete flow
            msg = await send_and_get_response(conv, fake.email())
            msg = await send_and_get_response(conv, "01/01/1990")
            msg = await send_and_get_response(conv, fake.city())

            msg = await click_and_refresh(msg, client, "Delete Profile")
            assert "deleted" in msg.text.lower()


@pytest.mark.asyncio
async def test_invalid_date_of_birth_is_rejected(tg_api_id, tg_api_hash, tg_bot_username):
    async with TelegramClient(SESSION_NAME, tg_api_id, tg_api_hash) as client:
        async with client.conversation(tg_bot_username, timeout=15) as conv:
            await conv.send_message("/start")
            msg = await conv.get_response()

            msg = await click_and_refresh(msg, client, "Create Profile")
            msg = await send_and_get_response(conv, fake.user_name())
            msg = await send_and_get_response(conv, fake.email())

            # Send a non-date string — should be rejected
            msg = await send_and_get_response(conv, "not-a-date")
            assert "invalid" in msg.text.lower() or "date" in msg.text.lower()

            # Recover: provide valid DOB and complete flow
            msg = await send_and_get_response(conv, "15/06/1990")
            msg = await send_and_get_response(conv, fake.city())

            msg = await click_and_refresh(msg, client, "Delete Profile")
            assert "deleted" in msg.text.lower()


@pytest.mark.asyncio
async def test_view_profile_when_none_exists(tg_api_id, tg_api_hash, tg_bot_username):
    async with TelegramClient(SESSION_NAME, tg_api_id, tg_api_hash) as client:
        async with client.conversation(tg_bot_username, timeout=10) as conv:
            await conv.send_message("/start")
            msg = await conv.get_response()

            # Ensure no profile exists
            msg = await click_and_refresh(msg, client, "Delete Profile")

            await conv.send_message("/start")
            msg = await conv.get_response()
            msg = await click_and_refresh(msg, client, "View Profile")

            assert "not found" in msg.text.lower() or "create" in msg.text.lower()


@pytest.mark.asyncio
async def test_delete_profile_when_none_exists(tg_api_id, tg_api_hash, tg_bot_username):
    async with TelegramClient(SESSION_NAME, tg_api_id, tg_api_hash) as client:
        async with client.conversation(tg_bot_username, timeout=10) as conv:
            # First delete to ensure clean state
            await conv.send_message("/start")
            msg = await conv.get_response()
            msg = await click_and_refresh(msg, client, "Delete Profile")

            # Try deleting again when already gone
            await conv.send_message("/start")
            msg = await conv.get_response()
            msg = await click_and_refresh(msg, client, "Delete Profile")

            assert "no profile" in msg.text.lower() or "not found" in msg.text.lower()
