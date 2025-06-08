import os
import sys
from dotenv import load_dotenv
from pyngrok import ngrok

# Set path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import dispatcher  # Import after setting sys.path

ENV_PATH = ".env"
PORT = 8443

def update_env_public_url(new_url: str):
    """Update PUBLIC_URL in .env file."""
    new_lines = []
    with open(ENV_PATH, "r") as f:
        for line in f:
            if line.startswith("PUBLIC_URL="):
                new_lines.append(f"PUBLIC_URL={new_url}\n")
            else:
                new_lines.append(line)
    with open(ENV_PATH, "w") as f:
        f.writelines(new_lines)
    print(f".env updated with PUBLIC_URL={new_url}")

def main():
    # 1. Start ngrok tunnel (bind_tls ensures HTTPS)
    print(f"Starting ngrok tunnel on port {PORT}...")
    tunnel = ngrok.connect(PORT, bind_tls=True)
    public_url = tunnel.public_url
    print(f"Ngrok tunnel URL: {public_url}")

    # 2. Update .env file with the new public URL
    update_env_public_url(public_url)

    # 3. Reload the updated .env
    load_dotenv(override=True)  # ✅ Force reloading updated values into os.environ

    # 4. Run the bot using the updated PUBLIC_URL
    print("Running your webhook setup and starting Flask server...")
    dispatcher.run_webhook()

if __name__ == "__main__":
    main()
