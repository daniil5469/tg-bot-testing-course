import requests
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def test_webhook_is_registered_and_healthy():
    logger.info("Checking Telegram webhook health via getWebhookInfo")

    response = requests.get(f"{TELEGRAM_API}/getWebhookInfo")
    logger.info("Telegram API status code: %s", response.status_code)

    assert response.status_code == 200

    data = response.json()
    logger.info("Webhook info response: %s", data)

    assert data["ok"] is True

    result = data["result"]

    logger.info("Webhook URL: %s", result.get("url"))
    logger.info("Pending updates: %s", result.get("pending_update_count"))
    logger.info("Last error message: %s", result.get("last_error_message"))

    assert result["url"], "Webhook URL is not set"
    assert result["pending_update_count"] == 0

    assert result.get("last_error_message") is None, (
        f"Telegram reports webhook error: {result.get('last_error_message')}"
    )

    logger.info("Webhook is registered and healthy")
