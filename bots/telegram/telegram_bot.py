from bots.bot_interface import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
import os
from dotenv import load_dotenv

load_dotenv()


class TelegramBot(Bot):
    """
    Concrete implementation of the Bot interface for Telegram.
    """

    def __init__(self):
        """
        Initializes the Telegram bot with its token and application.
        """
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.application = ApplicationBuilder().token(self.token).build()
        self.set_handlers()

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handles the /start command.
        """
        await update.message.reply_text("👋 Hello! Welcome to the job alert bot!")

    def set_handlers(self):
        """
        Registers command handlers with the Telegram application.
        """
        start_handler = CommandHandler("start", self.start_command)
        self.application.add_handler(start_handler)

    def send_message(self, chat_id: str, message: str):
        """
        Sends a text message to a specific chat ID.
        """
        self.application.bot.send_message(chat_id=chat_id, text=message)

    def run(self):
        """
        Starts the bot's polling mechanism.
        """
        print("🤖 Telegram bot is now running...")
        self.application.run_polling()
