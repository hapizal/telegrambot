# This script will check any new feed to file_update.txt, this file_update.txt will get any new message from any other script for checking the health status of the servers monitored
import os
import asyncio
import time
import telegram
from tenacity import retry, stop_after_attempt, wait_fixed

# Telegram bot token and group chat ID
TELEGRAM_BOT_TOKEN = 'BOT_TOKEN'
TELEGRAM_GROUP_CHAT_ID = '-CHATGROUPID'

# Initialize the bot
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

# File to monitor
file_path = 'file_update.txt'

# Keep track of the file size to detect new content
file_size = os.path.getsize(file_path)

# Send message to telegram chat group
async def send_telegram_message(message):
    await bot.send_message(chat_id=TELEGRAM_GROUP_CHAT_ID, text=message)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
async def monitor_file():
    global file_size

    while True:
        try:
            # Check if the file size has changed
            new_file_size = os.path.getsize(file_path)
            if new_file_size > file_size:
                # Read the new content
                with open(file_path, 'r') as file:
                    file.seek(file_size)
                    new_content = file.read()

                # Send the new content via Telegram
                await send_telegram_message(new_content)

                # Update the file size
                file_size = new_file_size

            # Wait for a short period before checking again
            await asyncio.sleep(1)

        except Exception as e:
            print(f"Exception occurred: {e}")
            continue

# Run the asyncio event loop
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(monitor_file())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
