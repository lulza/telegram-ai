from dotenv import load_dotenv
import bot
import os

if __name__ == "__main__":
    load_dotenv()
    telegram_key = os.getenv("TELEGRAM_API_KEY")
    bot_username = os.getenv("BOT_USERNAME")
    if telegram_key == "" or bot_username == "":
        print("TELEGRAM_API_KEY env is empty")
        exit(1)
    
    telebot = bot.Bot(telegram_key, bot_username)
    telebot.start()
