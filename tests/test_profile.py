import os
import json
import pytest
import sys
from src.services.user_store import save_user, delete_user_profile, get_user

print("\nsys.path:\n", "\n".join(sys.path), "\n")

DATA_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "src", "core", "data", "user_data.json"
)

@pytest.fixture
def mock_chat_id():
    return 99999999

@pytest.fixture
def user_data():
    return {
        "nickname": "test_user",
        "email": "test@example.com",
        "dob": "1990-01-01",
        "location": "Testville"
    }

@pytest.fixture(autouse=True)
def clean_user_data(mock_chat_id):
    yield
    delete_user_profile(mock_chat_id)

def test_save_and_get_user(mock_chat_id, user_data):
    print("Verify save_user, get_user")
    save_user(mock_chat_id, user_data)
    stored = get_user(mock_chat_id)
    assert stored == user_data
    assert isinstance(stored["nickname"], str)
    assert isinstance(stored["email"], str)
    assert isinstance(stored["dob"], str)
    assert isinstance(stored["location"], str)

def test_update_user_profile(mock_chat_id, user_data):
    print("Verify test_update_user_profile")
    save_user(mock_chat_id, user_data)
    updated_data = user_data.copy()
    updated_data["nickname"] = "updated_user"
    updated_data["location"] = "New City"
    save_user(mock_chat_id, updated_data)
    stored = get_user(mock_chat_id)
    assert stored["nickname"] == "updated_user"
    assert stored["location"] == "New City"

def test_invalid_user_returns_none():
    print("Verify test_invalid_user_returns_none")
    assert get_user(12345678) is None

def test_user_data_json_file_format(mock_chat_id, user_data):
    print("Verify test_user_data_json_file_format")
    save_user(mock_chat_id, user_data)
    with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    assert str(mock_chat_id) in raw_data
    profile = raw_data[str(mock_chat_id)]
    assert set(profile.keys()) == {"nickname", "email", "dob", "location"}

def test_delete_user_profile(mock_chat_id, user_data):
    print("Verify test_delete_user_profile")
    save_user(mock_chat_id, user_data)
    deleted = delete_user_profile(mock_chat_id)
    assert deleted is True
    assert get_user(mock_chat_id) is None
    with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    assert str(mock_chat_id) not in raw_data

def test_delete_non_existent_user():
    print("Verify test_delete_non_existent_user")
    assert delete_user_profile(12345678) is False
