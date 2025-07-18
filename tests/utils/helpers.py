import httpx
import os
import re
import time

def send_message(chat_id, text):
    token = os.getenv("BOT_TOKEN")
    base_url = os.getenv("BASE_URL")
    url = f"{base_url}/bot{token}/sendMessage"
    return httpx.post(url, json={"chat_id": chat_id, "text": text})

def read_log():
    log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bot.log"))
    with open(log_path, "r") as f:
        return f.read()

def wait_for_log(log_path, pattern, timeout=15, poll_interval=1):
    """
    Polls the given log file until the regex pattern is found or timeout is reached.
    Returns True if pattern is found, else False.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with open(log_path, "r") as f:
                content = f.read()
                if re.search(pattern, content):
                    return True
        except FileNotFoundError:
            pass  # file might not exist yet
        time.sleep(poll_interval)
    return False