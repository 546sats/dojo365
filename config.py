import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Scheduling Configuration
QUOTE_TIME = os.getenv('QUOTE_TIME', '06:00')
TIMEZONE = os.getenv('TIMEZONE', 'UTC')

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///quotes.db')

# Validation
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is required")
