# 🧑‍💻 Author

Made with 💙 for the Telegram API Testing Mini-Course
Follow along on my [LinkedIn](https://www.linkedin.com/in/daniil-shapovalov/) or Telegram channel @softwaretestersnotes 🎓

# 🤖 Testronaut Bot

Testronaut is a Telegram bot built as part of a mini-course on testing Telegram applications via API. It helps participants understand how Telegram bots work and how to write automated tests using Python.

# 🚀 Getting Started

Ensure you have latest python and pip installed

To run your own copy of this bot, follow these steps:

1. Create a new Telegram bot

Go to @BotFather in Telegram and create a bot:

```text
/start
/newbot
→ Choose a name and username for your bot
→ You’ll receive a bot token like: 123456789:ABCdefGhIJKlmNoPQRstuVWxyZ
```

2. Clone this repo to your working directory

```bash
git clone https://github.com/daniil5469/tg-bot-testing-course
cd tg-bot-testing-course
```

3. Create a .env file
In the project root, create a file named .env and add your token:

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRstuVWxyZ
```

⚠️ Never commit your `.env` file. It’s already listed in `.gitignore` to protect your token.

## 📁 Project Structure

![Project Structure image](assests/pproject_structure.png)

## 📌 Bot Features

- Create user profile (`nickname`, `email`, `date of birth`, `location`)
- Edit user profile
- Fetch cryptocurrency quotes in USD
- Add favorite currencies and edit the list

## 🛠️ Setup

```bash
# Once you cloned repo and added .env with TELEGRAM_BOT_TOKEN do next:

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
