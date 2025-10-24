"""
Helper script to get your Telegram Chat ID
Run this after sending a message to your bot
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_chat_id():
    """Get chat ID from Telegram API"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN not found in .env file")
        print("Please add your bot token to the .env file first")
        return
    
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if not data['ok']:
            print(f"❌ API Error: {data}")
            return
            
        if not data['result']:
            print("📱 No messages found. Please:")
            print("1. Open Telegram")
            print("2. Search for your bot")
            print("3. Send any message (like 'Hello' or '/start')")
            print("4. Run this script again")
            return
            
        print("✅ Found messages! Your Chat IDs:")
        print("-" * 50)
        
        chat_ids = set()
        for update in data['result']:
            if 'message' in update:
                chat_id = update['message']['chat']['id']
                chat_type = update['message']['chat']['type']
                user_name = update['message']['from'].get('first_name', 'Unknown')
                chat_ids.add((chat_id, chat_type, user_name))
        
        for chat_id, chat_type, user_name in chat_ids:
            print(f"Chat ID: {chat_id}")
            print(f"Type: {chat_type}")
            print(f"User: {user_name}")
            print("-" * 50)
            
        if chat_ids:
            print(f"\n💡 Add this to your .env file:")
            print(f"TELEGRAM_CHAT_ID={list(chat_ids)[0][0]}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    print("🔍 Getting your Telegram Chat ID...")
    print("Make sure you've sent a message to your bot first!")
    print()
    get_chat_id()
