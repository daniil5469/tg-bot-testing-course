import time
import os

def test_bot_reply_logged():
    log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bot.log"))
    assert os.path.exists(log_path), "❌ bot.log not found. Did you configure logging?"

    print("👉 Please send `/start` to your bot in Telegram within 15 seconds...")

    time.sleep(15)

    with open(log_path, "r") as f:
        content = f.read()

    assert "✅ Sent to" in content, "❌ No confirmation log found."
    assert "👋 Hello" in content, "❌ Expected greeting not found in bot reply log."

    print("✅ Bot reply to /start logged successfully.")
