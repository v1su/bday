import json
from datetime import datetime
from telegram import Bot
import os

def check_birthdays(file_path):
    # Get today's date in MM-DD format
    today = datetime.now().strftime("%m-%d")
    message = "🚫 No one's birthday is today. But don't worry! You can still add your birthday! 🎉\n\n💌 Do you want to add your birthday? Just let me know and I'll add it for you! 🎂"

    # Load the JSON database
    with open(file_path, 'r') as file:
        birthdays = json.load(file)

    # Check for birthdays
    birthday_people = [entry for entry in birthdays if entry["date"][5:] == today]

    if birthday_people:
        message = "🎉 **Today's Birthdays:**\n\n"
        for entry in birthday_people:
            name = entry["name"]
            date = entry["date"]
            message += f"- **{name}** 🎂 - *{date}*\n"
        message += "\n🥳 Let's wish them a fantastic day! 🎉"

    return message

def send_telegram_message(token, chat_id, message):
    bot = Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message)

if __name__ == "__main__":
    # Path to the JSON file
    file_path = "birthdays.json"

    # Telegram Bot Credentials from GitHub Secrets
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    # Generate the birthday message
    message = check_birthdays(file_path)

    # Send the message
    send_telegram_message(TELEGRAM_TOKEN, CHAT_ID, message)
