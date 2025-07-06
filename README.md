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
```

⚠️ Never commit your `.env` file. It’s already listed in `.gitignore` to protect your token.

### 3. Create bot.log file in the cloned project root 

`bot.log` captures the bot's response and all the necessary info to work with this project

# 🚀 Getting Started

Ensure you have latest python and pip installed

To run your own copy of this bot, follow these steps:

## ▶️ Run the Bot

### Option 1: Polling Mode (recommended for local/dev testing)

```bash
python -m scripts.start_ngrok_and_bot --mode polling
```

Once bot is started and working, you should see:

```bash
🤖 Polling mode started
```

### Option 2: Webhook Mode (requires ngrok)


```bash
python -m scripts.start_ngrok_and_bot --mode webhook
```

Once bot is started and listening for a webhook updates, you should see:

```bash
🌐 Webhook mode: listening on https://your-ngrok-url.ngrok-free.app/webhook
```

⚠️ Make sure ngrok is installed and accessible from command line.


# 🧪 Run Tests

This bot includes log-based integration tests using pytest. After you interact with the bot manually (e.g., send /start command), the tests will validate bot behavior by reading the bot.log

Once you started the bot, you can run tests

### 1. Send command to the Bot in Telegram

```Telegram
/start
```

### 2. Run tests

```bash
pytest -s tests/test_start.py
```

### 3. Example output for polling mode

```bash
tests/test_start.py --- Please send `/start` message to the bot within 15 seconds...
✅ Bot replied to /start message successfully - found in logs
```

Use -s to print live console outputs (helpful when reading log progress)

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
