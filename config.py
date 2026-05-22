import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot Configuration
# Get your bot token from @BotFather on Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Admin user ID (replace with your Telegram ID)
# You can get your ID by using @userinfobot or by sending /id to the bot
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))

# Bot settings
BOT_USERNAME = os.getenv("BOT_USERNAME")  # Optional: Your bot's username without @
