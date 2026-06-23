import requests
import os

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def test_get_me_returns_success():
    response = requests.get(f"{TELEGRAM_API}/getMe")

    assert response.status_code == 200


def test_get_me_response_is_ok():
    response = requests.get(f"{TELEGRAM_API}/getMe")
    data = response.json()

    assert data["ok"] is True


def test_get_me_returns_bot_identity():
    response = requests.get(f"{TELEGRAM_API}/getMe")
    data = response.json()
    result = data["result"]

    assert "id" in result
    assert "username" in result
    assert "first_name" in result
    assert result["is_bot"] is True


def test_get_me_bot_has_valid_id():
    response = requests.get(f"{TELEGRAM_API}/getMe")
    data = response.json()

    assert isinstance(data["result"]["id"], int)
    assert data["result"]["id"] > 0


def test_telegram_api_rejects_invalid_token():
    bad_api = "https://api.telegram.org/bot000000000:INVALID_TOKEN_HERE"
    response = requests.get(f"{bad_api}/getMe")
    data = response.json()

    assert response.status_code == 401
    assert data["ok"] is False
