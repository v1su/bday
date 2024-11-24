import json
import os
from datetime import datetime
from telegram import Bot
from telegram.ext import Application
from telegram.error import TelegramError

async def check_birthdays(file_path):
    """
    Check for birthdays in the JSON file and return the appropriate message.
    """
    today = datetime.now().strftime("%m-%d")
    message = "🚫 No one's birthday is today. But don't worry! You can still add your birthday! 🎉\n\n💌 Do you want to add your birthday? Just let me know and I'll add it for you! 🎂"

    try:
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

    except FileNotFoundError:
        message = "❗ Error: Birthday database file not found!"
    except json.JSONDecodeError:
        message = "❗ Error: There was an issue reading the birthday database file. Please check the JSON format."
    except Exception as e:
        message = f"❗ An unexpected error occurred: {str(e)}"
    
    return message

async def send_telegram_message(token, chat_id, message):
    """
    Send a message to a Telegram chat.
    """
    try:
        # Initialize the bot using the provided token
        application = Application.builder().token(token).build()

        # Send the message asynchronously
        await application.bot.send_message(chat_id=chat_id, text=message)

    except TelegramError as e:
        print(f"Telegram error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    # Path to the JSON file (You should change this path if needed)
    file_path = "birthdays.json"

    # Telegram Bot Credentials from environment variables (set in GitHub secrets)
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    if TELEGRAM_TOKEN is None or CHAT_ID is None:
        print("❗ Error: Telegram Bot Token or Chat ID not found in environment variables.")
    else:
        # Generate the birthday message
        message = await check_birthdays(file_path)

        # Send the message
        await send_telegram_message(TELEGRAM_TOKEN, CHAT_ID, message)
