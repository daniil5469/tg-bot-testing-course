import requests
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def _mask_url(url: str) -> str:
    return "****" if url else None


def test_webhook_is_registered_and_healthy():
    logger.info("Checking Telegram webhook health via getWebhookInfo")

    response = requests.get(f"{TELEGRAM_API}/getWebhookInfo")
    logger.info("Telegram API status code: %s", response.status_code)

    assert response.status_code == 200

    data = response.json()
    masked_data = {
        **data,
        "result": {
            **data.get("result", {}),
            "url": "****" if data.get("result", {}).get("url") else None,
            "ip_address": "****" if data.get("result", {}).get("ip_address") else None,
        },
    }
    logger.info("Webhook info response: %s", masked_data)

    assert data["ok"] is True

    result = data["result"]

    webhook_url = result.get("url")
    masked_url = _mask_url(webhook_url) if webhook_url else None
    logger.info("Webhook URL: %s", masked_url)
    ip_address = result.get("ip_address")
    logger.info("IP address: %s", "****" if ip_address else None)
    logger.info("Pending updates: %s", result.get("pending_update_count"))
    logger.info("Last error message: %s", result.get("last_error_message"))

    assert result["url"], "Webhook URL is not set"
    assert result["pending_update_count"] == 0

    assert result.get("last_error_message") is None, (
        f"Telegram reports webhook error: {result.get('last_error_message')}"
    )

    logger.info("Webhook is registered and healthy")
