# Telegram Text Formatter Bot

A Telegram bot that helps format text for different platforms (Telegram, LinkedIn) with proper styling and formatting.

## Features

- Formats text for both Telegram and LinkedIn platforms
- Automatically formats headings with bold text
- Maintains proper numbered and bulleted lists
- Handles links in a clean, readable format
- Preserves text structure and spacing

## Local Setup & Running

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment:
   - Copy `.env.example` to `.env`
   - Add your Telegram Bot Token from [@BotFather](https://t.me/botfather)

4. Run the bot:
```bash
python main.py
```

## Bot Commands

- `/start` - Begin interaction and choose platform
- `/format` - Start new text formatting
- `/cancel` - Cancel current operation

## Usage

1. Start a chat with your bot on Telegram
2. Use `/start` or `/format` command
3. Choose your target platform (Telegram/LinkedIn)
4. Send your text
5. Receive the formatted version

## Formatting Features

- **Headings**: Automatically detected and bolded
- **Lists**: Proper numbering and bullet points
- **Links**: Clean, readable format
- **Text Structure**: Maintains paragraphs and spacing

## Requirements

- Python 3.11+
- python-telegram-bot==20.3
- python-dotenv==1.0.0 