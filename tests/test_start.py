from utils.helpers import wait_for_log
import os

def test_start_command_reply_logged():
    log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bot.log"))
    pattern = r"✅ Sent greeting to user \d+: 👋 Hello, .+! Welcome to Testronaut Bot\."

    print("--- Please send `/start` message to the bot within 15 seconds...")

    success = wait_for_log(log_path, pattern, timeout=15)

    if success:
        print("✅ Bot replied to /start message successfully - found in logs")
    else:
        with open(log_path, "r") as f:
            print("❌ Pattern not found in logs. Full log content:\n", f.read())
        assert False, "❌ Expected bot greeting not found in logs"
