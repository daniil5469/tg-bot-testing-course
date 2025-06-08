# conftest.py
import os
from dotenv import load_dotenv
import pytest

# Load .env file once at the start of the test session
load_dotenv()

@pytest.fixture(scope="session")
def bot_token():
    return os.getenv("BOT_TOKEN")

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL")

@pytest.fixture(scope="session")
def test_user_chat_id():
    return os.getenv("TEST_CHAT_ID")
