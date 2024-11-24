import json
import os
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import RPCError
import logging
logging.basicConfig(level=logging.INFO)
logging.info("Bot started")

# Ensure you have your Telegram Bot Token and API credentials set in environment variables
# Set these environment variables either in your system or directly in the script
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_ID = int(os.getenv("TELEGRAM_API_ID"))
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))

def format_date_full(date):
    """
    Convert a date in YYYY-MM-DD format to a more readable format like '23 September 2000'.
    """
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
        return parsed_date.strftime("%d %B %Y")  # e.g., '23 September 2000'
    except ValueError:
        # Handle dates without the year
        parsed_date = datetime.strptime(date, "%m-%d")
        return parsed_date.strftime("%d %B")  # e.g., '23 September'

async def check_birthdays(file_path):
    """
    Check for birthdays in the JSON file and return the appropriate message.
    """
    today = datetime.now().strftime("%m-%d")
    full_today = datetime.now().strftime("%d %B %Y")  # Full date format for today
    message = (
        f"🌞 **Good Day! Today is {full_today}.**\n\n"
        "🚫 *No birthdays today!* 🎂 But every day is special, so why not spread some joy and make someone smile today? 🌟\n\n"
        "✨ Remember, life is worth celebrating every single day! 💫\n\n"
        "💌 Want to add your birthday to the list? Let me know, and we’ll make sure you get the spotlight when your day arrives! 🎉"
    )

    try:
        # Load the JSON database
        with open(file_path, "r") as file:
            birthdays = json.load(file)

        # Check for birthdays
        birthday_people = [entry for entry in birthdays if entry["date"][5:] == today]

        if birthday_people:
            message = "✨🎉 **🎂 Happy Birthday! 🎂** 🎉✨\n\n"
            for entry in birthday_people:
                name = entry["name"]
                birth_date = entry["date"]

                # Format the date with full details
                formatted_date = format_date_full(birth_date)

                # If year is included, calculate age
                if len(birth_date) == 10:  # Format YYYY-MM-DD
                    birth_year = int(birth_date[:4])
                    current_year = datetime.now().year
                    age = current_year - birth_year
                    message += (
                        f"🎁 **{name}** 🎉\n"
                        f"🎂 Born on: *{formatted_date}*\n"
                        f"🌟 Turns **{age} years old** today! 🥳\n\n"
                    )
                else:
                    message += (
                        f"🎁 **{name}** 🎉\n"
                        f"🎂 Born on: *{formatted_date}*\n"
                        f"✨ Let's make their day amazing! 🌈\n\n"
                    )

            message += "🎊 Don't forget to send them your warmest wishes! 💌\n\n"
            message += "🎉 *Celebrate like there's no tomorrow!* 🥂"

    except FileNotFoundError:
        message = "❗ Error: Birthday database file not found!"
    except json.JSONDecodeError:
        message = "❗ Error: There was an issue reading the birthday database file. Please check the JSON format."
    except Exception as e:
        message = f"❗ An unexpected error occurred: {str(e)}"

    return message

async def send_telegram_message(client, chat_id, message):
    """
    Send a message to a Telegram chat.
    """
    try:
        await client.send_message(chat_id, message)
    except RPCError as e:
        print(f"Telegram RPC error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

async def main():
    """
    Main function that gets the birthday message and sends it to Telegram.
    """
    # Path to the JSON file (You should change this path if needed)
    file_path = "birthdays.json"

    if TELEGRAM_BOT_TOKEN is None or TELEGRAM_API_ID is None or TELEGRAM_API_HASH is None or TELEGRAM_CHAT_ID is None:
        print("❗ Error: Telegram Bot Token, API ID, API Hash, or Chat ID not found in environment variables.")
    else:
        # Use Bot Token for authentication if available
        client = TelegramClient("birthday_notifier", TELEGRAM_API_ID, TELEGRAM_API_HASH)

        # Use the bot token for authentication if it's a bot
        await client.start(bot_token=TELEGRAM_BOT_TOKEN)

        # Generate the birthday message
        message = await check_birthdays(file_path)

        # Send the message
        await send_telegram_message(client, TELEGRAM_CHAT_ID, message)
        await client.disconnect()  # Disconnect after sending the message

# Run the async code
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
