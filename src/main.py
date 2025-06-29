import sys
from src.core.dispatcher import run_bot, run_webhook

if __name__ == "__main__":
    mode = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--mode" else "polling"

    if mode == "polling":
        run_bot()
    elif mode == "webhook":
        run_webhook()
    else:
        print("Invalid mode. Use --mode polling or --mode webhook.")
