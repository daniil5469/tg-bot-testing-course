from dotenv import load_dotenv
import subprocess
import time
import requests

PORT = 8443
ENV_PATH = ".env"

def start_ngrok_once():
    try:
        tunnels = requests.get("http://127.0.0.1:4040/api/tunnels").json().get("tunnels", [])
        if tunnels:
            print("🔁 Ngrok already running. Reusing tunnel.")
            return tunnels[0]["public_url"]
    except Exception:
        print("ℹ️ No existing ngrok tunnel found. Starting manually...")

    # Start ngrok in background
    subprocess.Popen(["ngrok", "http", str(PORT)], stdout=subprocess.DEVNULL)
    print("🚀 Ngrok process started via subprocess...")

    # Wait for ngrok to come up
    time.sleep(3)

    # Get the newly created ngrok public URL (for current session)
    tunnels = requests.get("http://127.0.0.1:4040/api/tunnels").json()["tunnels"]
    public_url = tunnels[0]["public_url"]
    return public_url

def update_env_public_url(public_url):
    new_lines = []
    with open(ENV_PATH, "r") as f:
        for line in f:
            if line.startswith("PUBLIC_URL="):
                new_lines.append(f"PUBLIC_URL={public_url}\n")
            else:
                new_lines.append(line)
    with open(ENV_PATH, "w") as f:
        f.writelines(new_lines)
    print(f".env updated with PUBLIC_URL={public_url}")

def update_ngrok_env():
    public_url = start_ngrok_once()
    update_env_public_url(public_url)
    load_dotenv(override=True)  # So os.environ is updated
    return public_url
