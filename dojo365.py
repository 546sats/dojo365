"""
DOJO365 - Daily Philosophy Quote Bot
A Telegram bot that sends daily philosophy quotes for reflection and personal growth.
"""

import requests
import time
import schedule
import threading
import json
import os
import datetime

class DOJO365Bot:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.last_update_id = 0
        self.user_times = {}
        self.all_users = set()
        self.user_timezones = {}
    
    def get_quote_emoji(self, author):
        """Get appropriate emoji based on author"""
        emoji_map = {
            'Marcus Aurelius': '🏛️',
            'Epictetus': '⚡',
            'Seneca': '📜',
            'Plato': '🔮',
            'Aristotle': '🎯',
            'Socrates': '💭',
            'Buddha': '🧘',
            'Lao Tzu': '☯️',
            'Confucius': '📚',
            'Friedrich Nietzsche': '🔥',
            'Carl Jung': '🌙',
            'Viktor Frankl': '💪',
            'Sun Tzu': '⚔️',
            'Rumi': '💫',
            'Albert Camus': '☀️',
            'Henry David Thoreau': '🌲',
            'Ralph Waldo Emerson': '🌅'
        }
        return emoji_map.get(author, '💭')
    
    def get_sample_quotes(self):
        """Sample quotes for demonstration"""
        return [
            {
                "quote": "The happiness of your life depends upon the quality of your thoughts.",
                "author": "Marcus Aurelius",
                "source": "Meditations"
            },
            {
                "quote": "It is not what happens to you, but how you react to it that matters.",
                "author": "Epictetus",
                "source": "Enchiridion"
            },
            {
                "quote": "Life is very short and anxious for those who forget the past, neglect the present, and fear the future.",
                "author": "Seneca",
                "source": "Letters from a Stoic"
            },
            {
                "quote": "The unexamined life is not worth living.",
                "author": "Socrates",
                "source": "Plato's Apology"
            },
            {
                "quote": "The way to get started is to quit talking and begin doing.",
                "author": "Walt Disney",
                "source": "Motivational Quote"
            }
        ]
    
    def get_random_quote(self):
        """Get a random quote from sample quotes"""
        import random
        quotes = self.get_sample_quotes()
        return random.choice(quotes)
    
    def send_message(self, text, chat_id=None, parse_mode='Markdown'):
        """Send a message to the chat"""
            target_chat_id = chat_id or self.chat_id
            if not target_chat_id:
                print("Error: No chat_id provided")
                return None
                
        url = f"{self.base_url}/sendMessage"
        data = {
                'chat_id': target_chat_id,
            'text': text,
            'parse_mode': parse_mode
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    message_id = result.get('result', {}).get('message_id')
                    print(f"Message sent successfully with ID: {message_id}")
                    return message_id
                else:
                    print(f"Telegram API error: {result}")
            else:
                print(f"HTTP error: {response.status_code}")
            return None
        except Exception as e:
            print(f"Error sending message: {e}")
            return None
    
    def send_message_with_keyboard(self, text, chat_id=None, keyboard=None):
        """Send a message with inline keyboard"""
            target_chat_id = chat_id or self.chat_id
            if not target_chat_id:
                print("Error: No chat_id provided")
                return None
                
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': target_chat_id,
                'text': text,
                'parse_mode': 'HTML'
            }
            if keyboard:
                data['reply_markup'] = json.dumps(keyboard)
            
            try:
                response = requests.post(url, data=data)
                if response.status_code == 200:
                    result = response.json()
                    if result.get('ok'):
                        message_id = result.get('result', {}).get('message_id')
                        print(f"Message with keyboard sent successfully with ID: {message_id}")
                        return message_id
                    else:
                        print(f"Telegram API error: {result}")
                else:
                    print(f"HTTP error: {response.status_code}")
                return None
            except Exception as e:
                print(f"Error sending message with keyboard: {e}")
                return None

    def build_timezone_keyboard(self):
        """Build timezone selection keyboard"""
        keyboard = {
            "inline_keyboard": [
                [{"text": "🌐 UTC (GMT+0)", "callback_data": "tz_+00:00"}],
                [{"text": "🇪🇺 Europe (+1 to +3)", "callback_data": "tz_region_europe"}],
                [{"text": "🇺🇸 America (-8 to -3)", "callback_data": "tz_region_america"}],
                [{"text": "🇦🇺 Asia Pacific (+5 to +12)", "callback_data": "tz_region_asia"}]
            ]
        }
        return keyboard
    
    def build_time_selection_keyboard(self):
        """Build time selection keyboard"""
        times = ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00"]
        rows = []
        row = []
        for i, time_str in enumerate(times, 1):
            row.append({"text": time_str, "callback_data": f"time_{time_str}"})
            if i % 4 == 0:
                rows.append(row)
                row = []
        if row:
            rows.append(row)
        
        rows.append([{"text": "⚙️ Custom time", "callback_data": "time_custom"}])
        return {"inline_keyboard": rows}
    
    def get_updates(self):
        """Get new messages from Telegram"""
        url = f"{self.base_url}/getUpdates"
        params = {'offset': self.last_update_id + 1, 'timeout': 5}
        try:
            response = requests.get(url, params=params)
            result = response.json()
            if result.get('ok'):
                updates_count = len(result.get('result', []))
                if updates_count > 0:
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    print(f"[{current_time}] Got {updates_count} updates")
            return result
        except Exception as e:
            print(f"Error getting updates: {e}")
            return None
    
    def handle_command(self, command, chat_id, message_text=None):
        """Handle bot commands"""
        log_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{log_time}] Handling command: {command} from chat: {chat_id}")
        
        if command == '/start':
            welcome_message = """🥋 <b>Welcome to DOJO365</b>

<i>Your daily dose of timeless wisdom.</i>

💡 <b>Features:</b>
• Daily philosophy quotes
• Timezone support
• Interactive setup
• Manual quote requests

🔧 <b>Commands:</b>
/quote - Get wisdom now
/time - Set daily time
/timezone - Set timezone
/help - More info

@dojo365_bot"""
            
            buttons_keyboard = {
                "inline_keyboard": [
                    [{"text": "💭 Get Quote Now", "callback_data": "get_quote"}],
                    [{"text": "🌍 Set Timezone", "callback_data": "change_timezone"}],
                    [{"text": "🕕 Set Time", "callback_data": "change_time"}]
                ]
            }
            
            self.send_message_with_keyboard(welcome_message, chat_id, buttons_keyboard)
            
        elif command == '/quote':
            quote_data = self.get_random_quote()
            emoji = self.get_quote_emoji(quote_data['author'])

            quote_text = f"""{emoji} "{quote_data['quote']}"

— {quote_data['author']}
{quote_data['source']}

@dojo365_bot"""
            self.send_message(quote_text, chat_id, parse_mode=None)
            
        elif command == '/help':
            help_text = """🥋 DOJO365 Commands

📋 Available Commands:
/quote - Get wisdom now
/time - Set daily time
/timezone - Set timezone
/help - Show this menu

💡 Features:
• Daily automated quotes
• Timezone support
• Interactive buttons
• Manual quote requests

@dojo365_bot"""
            self.send_message(help_text, chat_id, parse_mode=None)
            
        elif command == '/timezone':
                tz_message = """🌍 <b>Timezone Settings</b>

Choose your timezone for accurate delivery:"""
            tz_keyboard = self.build_timezone_keyboard()
                self.send_message_with_keyboard(tz_message, chat_id, tz_keyboard)

        elif command == '/time':
            time_message = """🕕 <b>Set Daily Time</b>

Choose when you want to receive daily quotes:"""
                    time_keyboard = self.build_time_selection_keyboard()
                    self.send_message_with_keyboard(time_message, chat_id, time_keyboard)
                    
    def handle_callback_query(self, callback_data, chat_id, callback_query_id):
        """Handle callback queries from inline keyboards"""
        if callback_data == "get_quote":
            quote_data = self.get_random_quote()
            emoji = self.get_quote_emoji(quote_data['author'])
            quote_text = f"""{emoji} "{quote_data['quote']}"

— {quote_data['author']}
{quote_data['source']}

@dojo365_bot"""
            self.send_message(quote_text, chat_id, parse_mode=None)
            self.answer_callback_query(callback_query_id)
            
        elif callback_data == "change_timezone":
            tz_message = """🌍 <b>Change Timezone</b>

Choose your timezone for accurate delivery:"""
            tz_keyboard = self.build_timezone_keyboard()
            self.send_message_with_keyboard(tz_message, chat_id, tz_keyboard)
            self.answer_callback_query(callback_query_id)
            
        elif callback_data == "change_time":
            time_message = """🕕 <b>Change Daily Time</b>

Choose when you want to receive daily quotes:"""
            time_keyboard = self.build_time_selection_keyboard()
            self.send_message_with_keyboard(time_message, chat_id, time_keyboard)
            self.answer_callback_query(callback_query_id)
            
        elif callback_data.startswith('time_'):
            time_str = callback_data[5:]
            if time_str == "custom":
                custom_message = """📝 <b>Custom Time</b>

Use: /time HH:MM
Example: /time 08:30"""
                self.send_message(custom_message, chat_id, parse_mode='HTML')
            else:
                success_message = f"""✅ <b>Time set to {time_str}</b>

Daily quotes will arrive at this time."""
                self.send_message(success_message, chat_id, parse_mode='HTML')
                self.answer_callback_query(callback_query_id, f"Time set to {time_str}")
            
        elif callback_data.startswith('tz_'):
            tz_str = callback_data[3:]
            if tz_str in ['+00:00', '+01:00', '+02:00', '+03:00', '-05:00', '-08:00']:
                success_message = f"""✅ <b>Timezone set to {tz_str}</b>

Your quotes will be delivered at the correct local time."""
                self.send_message(success_message, chat_id, parse_mode='HTML')
                self.answer_callback_query(callback_query_id, f"Timezone set to {tz_str}")
    
    def answer_callback_query(self, callback_query_id, text=None):
        """Answer a callback query to remove loading state"""
        url = f"{self.base_url}/answerCallbackQuery"
        data = {'callback_query_id': callback_query_id}
        if text:
            data['text'] = text
        try:
            requests.post(url, data=data)
        except Exception as e:
            print(f"Error answering callback query: {e}")
    
    def run_bot(self):
        """Main bot loop"""
        print("Starting DOJO365 - Philosophy Quote Bot")
        print("Bot is now running! Press Ctrl+C to stop.")
        
        try:
            while True:
                updates = self.get_updates()
                if updates and updates.get('ok'):
                    result_updates = updates.get('result', [])
                    
                    for update in result_updates:
                        update_id = update['update_id']
                        
                        if update_id > self.last_update_id:
                            self.last_update_id = update_id
                            
                            if 'message' in update:
                                message = update['message']
                                text = message.get('text', '')
                                chat_id = message['chat']['id']
                                self.all_users.add(str(chat_id))
                                print(f"Received message: '{text}' from user: {chat_id}")
                                
                                if text.startswith('/'):
                                    command = text.split()[0]
                                    print(f"Executing command: {command} from chat: {chat_id}")
                                    self.handle_command(command, chat_id, text)
                                else:
                                    print(f"Ignoring non-command message")
                            
                            elif 'callback_query' in update:
                                callback_query = update['callback_query']
                                callback_data = callback_query.get('data', '')
                                callback_query_id = callback_query.get('id', '')
                                chat_id = callback_query['message']['chat']['id']
                                self.all_users.add(str(chat_id))
                                print(f"Received callback: '{callback_data}' from chat: {chat_id}")
                                self.handle_callback_query(callback_data, chat_id, callback_query_id)
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nBot stopped by user")

def main():
    """Main function to run the bot"""
    bot = DOJO365Bot()
    bot.run_bot()

if __name__ == '__main__':
    main()