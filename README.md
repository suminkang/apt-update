# Apartment Listing Monitor

This bot monitors a specific website for new apartment listings and sends notifications via Telegram when new listings are found.

## Features

- Checks for new apartment listings every 5 minutes
- Sends notifications via Telegram
- Maintains a history of seen listings to avoid duplicates
- Runs automatically using GitHub Actions

## Setup

1. Fork this repository
2. Set up your Telegram bot:
   - Create a new bot using [@BotFather](https://t.me/botfather) on Telegram
   - Save the bot token
   - Start a chat with your bot
   - Get your chat ID by sending a message to [@userinfobot](https://t.me/userinfobot)

3. Add repository secrets:
   - Go to your repository's Settings > Secrets and variables > Actions
   - Add two new secrets:
     - `BOT_TOKEN`: Your Telegram bot token
     - `CHAT_ID`: Your Telegram chat ID

4. The GitHub Action will automatically start running every 5 minutes

## Local Development

To run the script locally:

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your credentials:
   ```
   BOT_TOKEN=your_bot_token_here
   CHAT_ID=your_chat_id_here
   ```
5. Run the script:
   ```bash
   python check_listings.py
   ```

## License

MIT 