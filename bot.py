import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import BOT_TOKEN, ADMIN_ID

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store user data
user_data = {}

k# Test sections and subjects data
test_sections = {
    "math": "Matematika",
    "physics": "Fizika",
    "chemistry": "Kimyo",
    "biology": "Biologiya",
    "history": "Tarix",
    "geography": "Geografiya",
    "literature": "Adabiyot",
    "english": "Ingliz tili",
    "informatics": "Informatika"
}

test_subjects = {
    "math": ["Algebra", "Geometriya", "Trigonometriya", "Statistika"],
    "physics": ["Mexanika", "Termodinamika", "Elektr", "Optika"],
    "chemistry": ["Organik kimyo", "Anorganik kimyo", "Biokimyo"],
    "biology": ["Sitologiya", "Genetika", "Ekologiya", "Anatomiya"],
    "history": ["O'zbekiston tarixi", "Jahon tarixi", "Madaniyat tarixi"],
    "geography": ["Fizik geografiya", "Iqtisodiy geografiya", "O'zbekiston geografiyasi"],
    "literature": ["Milliy adabiyot", "Jahon adabiyoti", "She'riyat"],
    "english": ["Grammar", "Vocabulary", "Reading", "Writing"],
    "informatics": ["Python", "Algoritmlar", "Ma'lumotlar tuzilmasi", "Web dasturlash"]
}

class Bot:
    def __init__(self):
        self.application = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup all bot handlers"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("id", self.id_command))
        self.application.add_handler(CommandHandler("info", self.info_command))
        self.application.add_handler(CommandHandler("admin", self.admin_command))
        self.application.add_handler(CommandHandler("broadcast", self.broadcast_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("clear", self.clear_command))
        self.application.add_handler(CommandHandler("sections", self.sections_command))
        self.application.add_handler(CommandHandler("subjects", self.subjects_command))
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        username = update.effective_user.username or "Anonymous"
        
        # Store user data
        if user_id not in user_data:
            user_data[user_id] = {
                "username": username,
                "message_count": 0,
                "first_seen": update.effective_user.first_name
            }
        
        welcome_message = f"""
🤖 **Welcome to the Bot!**

👤 User: {update.effective_user.first_name}
🆔 ID: `{user_id}`
🔖 Username: @{username}

Use /help to see all available commands.
        """
        
        keyboard = [
            [InlineKeyboardButton("📊 My Stats", callback_data=f"stats_{user_id}")],
            [InlineKeyboardButton("📚 Test Sections", callback_data="sections")],
            [InlineKeyboardButton("ℹ️ Help", callback_data="help")],
            [InlineKeyboardButton("🆔 My ID", callback_data=f"id_{user_id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, parse_mode='Markdown', reply_markup=reply_markup)
        logger.info(f"User {username} (ID: {user_id}) started the bot")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
📚 **Available Commands:**

🔹 `/start` - Start the bot
🔹 `/help` - Show this help message
🔹 `/id` - Get your Telegram ID
🔹 `/info` - Get detailed information about you
🔹 `/admin` - Admin commands (admin only)
🔹 `/broadcast <message>` - Broadcast message to all users (admin only)
🔹 `/stats` - Show bot statistics (admin only)
🔹 `/clear` - Clear your data

💡 Just send any text message and I'll echo it back!
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def id_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /id command"""
        user_id = update.effective_user.id
        await update.message.reply_text(f"🆔 Your Telegram ID: `{user_id}`", parse_mode='Markdown')
    
    async def info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /info command"""
        user = update.effective_user
        user_id = user.id
        
        info_text = f"""
👤 **User Information:**

📛 Name: {user.first_name} {user.last_name or ''}
🆔 ID: `{user_id}`
🔖 Username: @{user.username or 'N/A'}
🌐 Language: {user.language_code or 'N/A'}
🤖 Is Bot: {user.is_bot}
📊 Messages Sent: {user_data.get(user_id, {}).get('message_count', 0)}
        """
        await update.message.reply_text(info_text, parse_mode='Markdown')
    
    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /admin command (admin only)"""
        user_id = update.effective_user.id
        
        if user_id != ADMIN_ID:
            await update.message.reply_text("⛔ You don't have permission to use this command.")
            return
        
        admin_text = """
🔧 **Admin Commands:**

🔹 `/broadcast <message>` - Send message to all users
🔹 `/stats` - Show bot statistics
🔹 `/clear` - Clear all user data

Use these commands carefully!
        """
        await update.message.reply_text(admin_text, parse_mode='Markdown')
    
    async def broadcast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /broadcast command (admin only)"""
        user_id = update.effective_user.id
        
        if user_id != ADMIN_ID:
            await update.message.reply_text("⛔ You don't have permission to use this command.")
            return
        
        if not context.args:
            await update.message.reply_text("Usage: /broadcast <message>")
            return
        
        message = ' '.join(context.args)
        success_count = 0
        fail_count = 0
        
        for uid in user_data.keys():
            try:
                await context.bot.send_message(chat_id=uid, text=f"📢 **Broadcast:**\n\n{message}", parse_mode='Markdown')
                success_count += 1
            except Exception as e:
                logger.error(f"Failed to send to {uid}: {e}")
                fail_count += 1
        
        await update.message.reply_text(
            f"✅ Broadcast sent!\n\n"
            f"✓ Success: {success_count}\n"
            f"✗ Failed: {fail_count}"
        )
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command (admin only)"""
        user_id = update.effective_user.id
        
        if user_id != ADMIN_ID:
            await update.message.reply_text("⛔ You don't have permission to use this command.")
            return
        
        total_users = len(user_data)
        total_messages = sum(data.get('message_count', 0) for data in user_data.values())
        
        stats_text = f"""
📊 **Bot Statistics:**

👥 Total Users: {total_users}
💬 Total Messages: {total_messages}
📈 Average Messages per User: {total_messages / total_users if total_users > 0 else 0:.2f}
        """
        await update.message.reply_text(stats_text, parse_mode='Markdown')
    
    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /clear command"""
        user_id = update.effective_user.id
        
        if user_id == ADMIN_ID:
            user_data.clear()
            await update.message.reply_text("🗑️ All user data has been cleared.")
        else:
            if user_id in user_data:
                del user_data[user_id]
            await update.message.reply_text("🗑️ Your data has been cleared.")
    
    async def sections_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /sections command - show all test sections"""
        sections_text = "📚 **Test Bo'limlari:**\n\n"
        
        keyboard = []
        for key, name in test_sections.items():
            sections_text += f"🔹 {name}\n"
            keyboard.append([InlineKeyboardButton(name, callback_data=f"section_{key}")])
        
        keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="help")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(sections_text, parse_mode='Markdown', reply_markup=reply_markup)
    
    async def subjects_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /subjects command - show all subjects"""
        subjects_text = "📖 **Barcha Fanlar:**\n\n"
        
        for section, subjects in test_subjects.items():
            section_name = test_sections.get(section, section)
            subjects_text += f"📚 **{section_name}:**\n"
            for subject in subjects:
                subjects_text += f"  • {subject}\n"
            subjects_text += "\n"
        
        await update.message.reply_text(subjects_text, parse_mode='Markdown')
    
    async def show_section_subjects(self, update: Update, context: ContextTypes.DEFAULT_TYPE, section_key: str):
        """Show subjects for a specific section"""
        query = update.callback_query
        section_name = test_sections.get(section_key, section_key)
        subjects = test_subjects.get(section_key, [])
        
        if not subjects:
            await query.message.reply_text(f"❌ {section_name} uchun fanlar topilmadi.")
            return
        
        subjects_text = f"📚 **{section_name} Fanlari:**\n\n"
        for i, subject in enumerate(subjects, 1):
            subjects_text += f"{i}. {subject}\n"
        
        keyboard = []
        for subject in subjects:
            keyboard.append([InlineKeyboardButton(f"📝 {subject}", callback_data=f"test_{section_key}_{subject}")])
        keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="sections")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(subjects_text, parse_mode='Markdown', reply_markup=reply_markup)
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        user_id = update.effective_user.id
        
        if data == "help":
            help_text = """
📚 **Available Commands:**

🔹 `/start` - Start the bot
🔹 `/help` - Show this help message
🔹 `/id` - Get your Telegram ID
🔹 `/info` - Get detailed information about you
🔹 `/admin` - Admin commands (admin only)
🔹 `/broadcast <message>` - Broadcast message to all users (admin only)
🔹 `/stats` - Show bot statistics (admin only)
🔹 `/clear` - Clear your data
🔹 `/sections` - View all test sections
🔹 `/subjects` - View all subjects

💡 Just send any text message and I'll echo it back!
            """
            await query.message.reply_text(help_text, parse_mode='Markdown')
        elif data == "sections":
            sections_text = "📚 **Test Bo'limlari:**\n\n"
            
            keyboard = []
            for key, name in test_sections.items():
                sections_text += f"🔹 {name}\n"
                keyboard.append([InlineKeyboardButton(name, callback_data=f"section_{key}")])
            
            keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="help")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(sections_text, parse_mode='Markdown', reply_markup=reply_markup)
        elif data.startswith("id_"):
            user_id = update.effective_user.id
            await query.message.reply_text(f"🆔 Your Telegram ID: `{user_id}`", parse_mode='Markdown')
        elif data.startswith("stats_"):
            if user_id in user_data:
                stats = user_data[user_id]
                stats_text = f"""
📊 **Your Statistics:**

💬 Messages Sent: {stats.get('message_count', 0)}
👤 Username: @{stats.get('username', 'N/A')}
📛 First Name: {stats.get('first_seen', 'N/A')}
                """
                await query.message.reply_text(stats_text, parse_mode='Markdown')
            else:
                await query.message.reply_text("No data available. Use /start first.")
        elif data.startswith("section_"):
            section_name = data.replace("section_", "")
            await self.show_section_subjects(update, context, section_name)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages"""
        user_id = update.effective_user.id
        message_text = update.message.text
        
        # Update user data
        if user_id in user_data:
            user_data[user_id]['message_count'] += 1
        else:
            user_data[user_id] = {
                "username": update.effective_user.username or "Anonymous",
                "message_count": 1,
                "first_seen": update.effective_user.first_name
            }
        
        # Echo the message
        await update.message.reply_text(f"🔄 You said: {message_text}")
        logger.info(f"User {user_id} sent: {message_text}")
    
    def run(self):
        """Run the bot"""
        logger.info("Starting bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    bot = Bot()
    bot.run()
