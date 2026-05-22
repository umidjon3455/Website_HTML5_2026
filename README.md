# Telegram Bot with ID and Token Authentication

A comprehensive Telegram bot that uses ID and token for authentication with admin features, user statistics, and message broadcasting.

## Features

- **User Authentication**: Uses Telegram ID and token for secure access
- **Admin Commands**: Special commands for admin users only
- **User Statistics**: Track user activity and message counts
- **Message Broadcasting**: Send messages to all users (admin only)
- **Inline Keyboards**: Interactive buttons for better user experience
- **User Data Storage**: In-memory storage of user information
- **Echo Functionality**: Echoes back user messages

## Setup Instructions

### 1. Get Your Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token provided by BotFather

### 2. Get Your Telegram ID

1. Open Telegram and search for [@userinfobot](https://t.me/userinfobot)
2. Send any message to the bot
3. Copy your Telegram ID

### 3. Configure the Bot

1. Open `config.py`
2. Replace `YOUR_BOT_TOKEN_HERE` with your actual bot token
3. Replace `123456789` with your Telegram ID (for admin access)
4. Optionally, set `BOT_USERNAME` to your bot's username

```python
BOT_TOKEN = "your_actual_bot_token_here"
ADMIN_ID = 123456789  # Your Telegram ID
BOT_USERNAME = "your_bot_username"  # Optional
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Bot

```bash
python bot.py
```

## Available Commands

### User Commands
- `/start` - Start the bot and see welcome message
- `/help` - Show all available commands
- `/id` - Get your Telegram ID
- `/info` - Get detailed information about your account
- `/clear` - Clear your stored data

### Admin Commands (Admin ID only)
- `/admin` - Show admin-specific commands
- `/broadcast <message>` - Send a message to all users
- `/stats` - Show bot statistics (total users, messages, etc.)
- `/clear` - Clear all user data

## Features Explained

### ID and Token Authentication
- The bot uses your Telegram ID for user identification
- The bot token is used to authenticate with Telegram's API
- Admin commands are protected by checking the user ID against the configured ADMIN_ID

### User Statistics
- Tracks number of messages per user
- Stores username and first name
- Provides statistics via `/stats` command (admin) or inline buttons

### Broadcasting
- Admin can send messages to all registered users
- Shows success/failure count after broadcasting
- Useful for announcements and updates

### Inline Keyboards
- Interactive buttons for quick actions
- "My Stats" - View your personal statistics
- "Help" - Show help message
- "My ID" - View your Telegram ID

## Security Notes

- **Never share your bot token** - It gives full access to your bot
- **Keep your admin ID private** - Only you should have admin access
- **Data is stored in memory** - All user data is lost when the bot stops
- For production use, consider adding a database for persistent storage

## Troubleshooting

### Bot doesn't respond
- Check if the bot token is correct in `config.py`
- Ensure you've installed all dependencies
- Check if the bot is running without errors

### Admin commands don't work
- Verify your Telegram ID is correct in `config.py`
- Make sure you're using the correct Telegram account

### Dependencies installation fails
- Ensure you're using Python 3.7 or higher
- Try upgrading pip: `pip install --upgrade pip`
- Use a virtual environment: `python -m venv .venv`

## Future Enhancements

- Add database support (SQLite, PostgreSQL)
- Add user groups/roles
- Add file upload/download features
- Add scheduled messages
- Add webhook support for production deployment
- Add rate limiting
- Add more admin management features

## License

This project is open source and available for educational purposes.
