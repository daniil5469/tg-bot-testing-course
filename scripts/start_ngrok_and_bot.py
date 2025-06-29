import sys
from src.core.dispatcher import run_webhook, run_bot

def main():
    mode = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--mode" else "webhook"

    if mode == "webhook":
        run_webhook()
    else:
        run_bot()

if __name__ == "__main__":
    main()
