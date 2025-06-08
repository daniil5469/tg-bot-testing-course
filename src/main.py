import os
import argparse
from src.core.dispatcher import run_bot, run_webhook
from dotenv import load_dotenv

load_dotenv()  # Load .env once here

def parse_args():
    parser = argparse.ArgumentParser(description="Run Telegram bot in polling or webhook mode.")
    parser.add_argument(
        "--mode",
        choices=["polling", "webhook"],
        help="Set the bot mode (polling or webhook). Overrides MODE in .env",
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    mode = args.mode or os.getenv("MODE", "polling").lower()

    if mode == "webhook":
        run_webhook()
    else:
        run_bot()
