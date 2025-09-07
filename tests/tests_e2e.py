import os
import json
import pytest
from faker import Faker
from telethon import TelegramClient
from utils.helpers import click_and_refresh, send_and_get_response

API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")
BOT_USERNAME = os.getenv("TG_BOT_USERNAME")
PHONE = os.getenv("TG_PHONE")
SESSION_NAME = "user_session"

fake = Faker()

@pytest.fixture
def test_profile_data():
    dob_raw = fake.date_of_birth(minimum_age=18, maximum_age=50)
    return {
        "nickname": fake.user_name(),
        "email": fake.email(),
        "dob_raw": dob_raw,
        "dob": dob_raw.strftime("%d/%m/%Y"),   # e.g. "10/12/1998"
        "dob_formatted": dob_raw.isoformat(),  # e.g. "1998-12-10"
        "location": fake.city()
    }

@pytest.fixture
def expected_profile_text(test_profile_data):
    with open("tests/fixtures/expected_profile.json") as f:
        template = json.load(f)["template"]
    return template.format(
        nickname=test_profile_data["nickname"],
        email=test_profile_data["email"],
        dob=test_profile_data["dob_formatted"],  #instead of dob as it makes test failed due to foormatting
        location=test_profile_data["location"]
    )

@pytest.mark.asyncio
async def test_profile_creation_and_viewing(test_profile_data, expected_profile_text):
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        async with client.conversation(BOT_USERNAME) as conv:
            # Start bot
            await conv.send_message("/start")
            msg = await conv.get_response()

            # View profile (should be empty)
            msg = await click_and_refresh(msg, client, "View Profile")
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

            # Confirmation
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