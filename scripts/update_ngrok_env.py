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

    # Poll until tunnel is ready (up to 15 seconds)
    for _ in range(30):
        time.sleep(0.5)
        try:
            tunnels = requests.get("http://127.0.0.1:4040/api/tunnels").json().get("tunnels", [])
            if tunnels:
                public_url = tunnels[0]["public_url"]
                print(f"✅ Tunnel ready: {public_url}")
                return public_url
        except Exception:
            pass

    raise RuntimeError("ngrok tunnel did not start within 15 seconds")

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
