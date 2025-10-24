# 🧘 DOJO365 - Daily Philosophy Quote Bot

A Telegram bot that sends daily philosophy quotes for deep reflection and focus. Each day, you'll receive a carefully curated quote from great thinkers like Marcus Aurelius, Stoic philosophers, Eastern wisdom traditions, and modern psychology.

## ✨ Features

- **Daily Automated Quotes**: Receives one thoughtful quote per day at your chosen time
- **Manual Quote Requests**: Get quotes on-demand using `/quote` command
- **Timezone Support**: Set your timezone for accurate local delivery
- **Interactive Setup**: Easy timezone and time configuration with buttons
- **Diverse Philosophy Sources**: 
  - Ancient Greek & Roman (Stoics, Plato, Aristotle)
  - Eastern Philosophy (Taoism, Buddhism, Confucianism)
  - Samurai Philosophy (Hagakure, Book of Five Rings)
  - Modern Psychology & Philosophy (Jung, Frankl, Nietzsche)
  - Literary & Cultural Figures
  - Folk Wisdom & Proverbs

## 🚀 Live Demo

**Try the bot:** [@dojo365_bot](https://t.me/dojo365_bot)

## 🚀 Quick Start

### 1. Create a Telegram Bot

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Choose a name and username for your bot
4. Save the bot token you receive

### 2. Get Your Chat ID

1. Start a conversation with your bot
2. Send any message to your bot
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Find your chat ID in the response

### 3. Setup Environment

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/dojo365.git
   cd dojo365
   ```

2. Copy the environment template:
   ```bash
   cp env.example .env
   ```

3. Edit `.env` with your configuration:
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   QUOTE_TIME=06:00
   TIMEZONE=UTC
   ```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Bot

```bash
python dojo365.py
```

## 📱 Bot Commands

- `/start` - Welcome message and introduction
- `/quote` - Get a random philosophy quote for reflection
- `/time` - Set daily time & timezone
- `/timezone` - Set timezone only
- `/help` - Show help message

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from BotFather | Required |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID | Required |
| `QUOTE_TIME` | Daily quote time (24h format) | `06:00` |
| `TIMEZONE` | Timezone for scheduling | `UTC` |

### Customizing Quote Time

Edit the `QUOTE_TIME` in your `.env` file:
```env
QUOTE_TIME=07:30  # 7:30 AM
QUOTE_TIME=18:00  # 6:00 PM
```

## 🏗️ Project Structure

```
DOJO365/
├── dojo365.py           # Main bot logic and handlers
├── config.py            # Configuration management
├── get_chat_id.py       # Helper script for chat ID
├── requirements.txt     # Python dependencies
├── env.example         # Environment template
└── README.md           # This file
```

## 📚 Quote Sources

The bot includes quotes from:

- **Marcus Aurelius** - Meditations
- **Epictetus** - Enchiridion, Discourses
- **Seneca** - Letters from a Stoic, On the Shortness of Life
- **Yamamoto Tsunetomo** - Hagakure (The Way of the Samurai)
- **Miyamoto Musashi** - The Book of Five Rings
- **Lao Tzu** - Tao Te Ching
- **Confucius** - Analects
- **Buddha** - Dhammapada
- **Heraclitus** - Fragments
- **Socrates** - Plato's Apology
- **Aristotle** - Nicomachean Ethics, Metaphysics
- **Friedrich Nietzsche** - Twilight of the Idols
- **Viktor Frankl** - Man's Search for Meaning
- **Rumi** - The Essential Rumi
- **Sun Tzu** - The Art of War
- **Carl Jung** - The Red Book
- **And many more...**

## 🚀 Deployment Options

### Option 1: Local Development
Run the bot on your local machine for testing and personal use.

### Option 2: Cloud Deployment
Deploy to cloud platforms like:
- **Heroku**: Use the included `Procfile`
- **Railway**: Connect your GitHub repo
- **DigitalOcean**: Use App Platform
- **AWS**: Use EC2 or Lambda
- **Google Cloud**: Use Cloud Run

### Option 3: VPS Deployment
Deploy to a VPS using:
- **Docker**: Use the included `Dockerfile`
- **Systemd**: Create a service file
- **PM2**: Process manager for Node.js-like experience

## 🔧 Advanced Features

### Adding Custom Quotes

Edit `quotes_database.py` to add your own quotes:

```python
{
    "quote": "Your custom quote here",
    "author": "Author Name",
    "source": "Book/Source Name"
}
```

### Multiple Chat Support

The bot automatically tracks all users who interact with it and can send quotes to multiple users with their individual timezone and time preferences.

### Database Integration

For persistent storage and advanced features, you can integrate with:
- SQLite (simple)
- PostgreSQL (robust)
- MongoDB (flexible)

## 🛠️ Troubleshooting

### Common Issues

1. **Bot not responding**: Check your bot token and chat ID
2. **Quotes not sending**: Verify the time format and timezone
3. **Import errors**: Ensure all dependencies are installed

### Logs

The bot logs important events. Check the console output for:
- Successful quote deliveries
- Error messages
- Scheduling information

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add more philosophy quotes
- Improve the bot's functionality
- Fix bugs or improve documentation
- Suggest new features

## 🙏 Acknowledgments

- All the great philosophers whose wisdom is shared
- The python-telegram-bot library developers
- The open-source community

---

*"The unexamined life is not worth living."* - Socrates

Start your journey of daily reflection today! 🧘‍♂️
