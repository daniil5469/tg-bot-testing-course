from pyngrok import ngrok
import os
from dotenv import load_dotenv

load_dotenv()

# Start ngrok tunnel on your Flask port
port = 8443
tunnel = ngrok.connect(port, bind_tls=True)
public_url = tunnel.public_url  # ✅ Correct way to get the raw URL
print(f"🔥 Public URL: {public_url}")

# Update the .env file
env_path = ".env"
new_lines = []
with open(env_path, "r") as f:
    for line in f:
        if line.startswith("PUBLIC_URL="):
            new_lines.append(f"PUBLIC_URL={public_url}\n")
        else:
            new_lines.append(line)

with open(env_path, "w") as f:
    f.writelines(new_lines)

print("✅ .env updated with new PUBLIC_URL")
