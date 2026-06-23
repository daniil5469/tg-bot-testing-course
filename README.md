[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

# 🧑‍💻 Author

Made with 💙 for the Telegram API Testing Mini-Course
Follow along on my [LinkedIn](https://www.linkedin.com/in/daniil-shapovalov/) or Telegram channel @softwaretestersnotes 🎓

# 🤖 Testronaut Bot

Testronaut is a Telegram bot built as part of a mini-course on testing Telegram applications via API. It helps participants understand how Telegram bots work and how to write automated tests using Python.

# 🧠 How It Works

This Telegram bot supports two run modes:

- **Polling mode**: the bot regularly checks Telegram servers for updates.
- **Webhook mode**: Telegram sends updates to your bot via a public URL exposed using `ngrok`.

All user interactions (commands, button clicks) are logged into `bot.log`. Integration tests validate that expected actions appear in the logs after real user interaction.

---

# ⚙️ Prepare Environment

### 1. Clone the Repository

```bash
git clone https://github.com/daniil5469/tg-bot-testing-course
cd tg-bot-testing-course
```

### 2. Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

✅ Flask, httpx, pytest, python-dotenv, and other dependencies are included.


# 🔐 Bot Configuration (!!!)

### 1. Create your own Telegram Bot

Go to @BotFather in Telegram:

```text
/start
/newbot
```

→ Choose a name and username for your bot
→ You’ll receive a bot token like: 123456789:ABCdefGhIJKlmNoPQRstuVWxyZ

```text
123456789:ABCdefGhIJKlmNoPQRstuVWxyZ
```

### 2. Create .env file in the cloned project root 
E.g.

```.env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRstuVWxyZ
CHAT_ID=123456789
PUBLIC_URL=https://your-ngrok-url.ngrok-free.app
BASE_URL=https://api.telegram.org
MODE=webhook

# Telethon (required for E2E tests)
TG_API_ID=12345678
TG_API_HASH=your_api_hash_here
TG_PHONE=+1234567890
TG_BOT_USERNAME=@your_bot_username

# Webhook secret (optional but recommended)
WEBHOOK_SECRET_TOKEN=your_random_secret_here
```

⚠️ Never commit your `.env` file. It’s already listed in `.gitignore` to protect your token.

### 3. Create Telethon session (required for E2E tests)

E2E tests use [Telethon](https://github.com/LonamiWebs/Telethon) to simulate a real user interacting with the bot. Telethon authenticates as a **regular Telegram user**, not as a bot. This means you need:

- MTProto API credentials from [my.telegram.org](https://my.telegram.org) (`TG_API_ID`, `TG_API_HASH`)
- A real phone number (`TG_PHONE`) to receive the one-time verification code

Run this script **once** to create the session file:

```bash
python scripts/create_session.py
```

Telethon will send a verification code to your Telegram account. Enter it when prompted. A `user_session.session` file will be saved in the project root and reused on every subsequent test run — you won’t need to authenticate again unless the session expires.

> **Common error:** `UserIsBotError: Bots can’t send messages to other bots`
>
> This means the session file was created with a bot token instead of a phone number. Fix:
> ```bash
> rm user_session.session
> python scripts/create_session.py
> ```

### 4. Create bot.log file in the cloned project root 

`bot.log` captures the bot's response and all the necessary info to work with this project

# 🚀 Getting Started

Ensure you have latest python and pip installed

To run your own copy of this bot, follow these steps:

## ▶️ Run the Bot

### Mode A — Polling (recommended for local/dev testing)

```bash
python -m scripts.start_ngrok_and_bot --mode polling
```

Expected output:

```
🤖 Polling mode started
```

### Mode B — Webhook (requires ngrok)

```bash
python -m scripts.start_ngrok_and_bot --mode webhook
```

Expected output:

```
🌐 Webhook mode: listening on https://your-ngrok-url.ngrok-free.app/webhook
```

⚠️ Make sure ngrok is installed and accessible from the command line.

---

# 🧪 Run Tests

Start the bot first (in either mode), then run tests in a separate terminal.

Use `-s` to see live console output (log progress, assertions, etc.).

### Run all tests

```bash
pytest
```

### Run by layer

```bash
# Webhook integration — validates webhook registration and health
pytest tests/0_test_webhook.py -s

# Profile unit tests — mock-based, no bot required
pytest tests/1_test_profile_mock.py -s

# /start command — polling mode, real Telethon client
pytest tests/2_test_start_polling.py -s

# Crypto market + profile creation E2E
pytest tests/3_test_favorites.py -s

# Full E2E user journey (profile + favorites)
pytest tests/7_tests_e2e.py -s

# Integration tests (bot info, crypto API)
pytest tests/integration/ -s
```

## 📁 Project Structure

```
├── scripts/
│   ├── start_ngrok_and_bot.py   # Unified entrypoint
│   ├── update_ngrok_env.py      # Ngrok tunnel setup
│   ├── update_webhook.py        # Set Telegram webhook
├── src/
│   ├── core/             # Dispatcher, app setup
│   ├── handlers/         # Bot handlers (start, profile, crypto)
│   ├── services/         # User data management (CRUD operations with user profile and data)
│   ├── config.py         # Environment variables setup
│   ├── main.py           # App run setup
├── tests/
│   ├── utils/
│   │   ├── helpers.py           # Tests utils(helpers)
│   ├── conftest.py              # Test config
│   ├── test_profile.py          # Unit tests for profile functionality
│   ├── test_start.py            # Integration test (/start)
│   ├── conftest.py              # Test config
├── .env                         # Create your own (!)
├── requirements.txt             # Install existing dependencies (!)
├── bot.log                      # Read helpful logs
```

# 🧪 Test Philosophy

✅ Real user sends commands via Telegram
✅ bot.log captures the bot's response
✅ pytest reads logs and validates output
✅ Works with both polling and webhook modes
✅ No mocking required — real integration 🧐

This makes the framework scalable, realistic, and ready for CI pipelines in the future (with manual input or automated clients).


## 📌 Bot Features

- Create user profile (`nickname`, `email`, `date of birth`, `location`)
- Edit user profile
- Fetch cryptocurrency quotes in USD
- Add favorite currencies and edit the list
