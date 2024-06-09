from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import model
from logger import Logger

from typing import Final

command_start: Final = "start"
command_blenderbot: Final = "blenderbot"
command_mGPT: Final = "mgpt"

start_command_text: Final = """Welcome to AI chat-bot, here you can talk to one of LLMs"""


class Bot:
    def __init__(self, telegram_key, bot_username):
        self.logger = Logger()
        self.logger.info("Starting bot...")
        
        if telegram_key == "":
            raise Exception("Telegram key is empty")
        self.bot_username = bot_username

        self.app = Application.builder().token(telegram_key).build()
        self.register_handlers()

        self.models = dict()
    
    def get_model(self, chat_id: int) -> model.Model:
        if chat_id not in self.models.keys():
            self.models[chat_id] = model.Model()
            self.logger.info(f"registered new {self.models[chat_id].model_type} model by user {chat_id}")
        return self.models[chat_id]
    
    def start(self):
        self.logger.info("Polling...")
        self.app.run_polling()
    
    def register_handlers(self):
        # commands handlers
        self.app.add_handler(CommandHandler(command_start, self.start_command))
        self.app.add_handler(CommandHandler(command_blenderbot, self.blenderbot_command))
        self.app.add_handler(CommandHandler(command_mGPT, self.mGPT_command))
        # message handler
        self.app.add_handler(MessageHandler(filters.TEXT, self.handle_message))
        # error handler
        self.app.add_error_handler(self.error)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(start_command_text)

    async def blenderbot_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.log_update(update)
        self.get_model(update.message.chat_id).load_model(model.blenderbot)

        welcome_text = self.get_model(update.message.chat_id).get_welcome_message()
        await update.message.reply_text(welcome_text)

    async def mGPT_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.log_update(update)
        self.get_model(update.message.chat_id).load_model(model.mGPT)

        welcome_text = self.get_model(update.message.chat_id).get_welcome_message()
        await update.message.reply_text(welcome_text)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.log_update(update)
        text: str = update.message.text
        chat_id: int = update.message.chat_id
        if update.message.chat.type == "group":
            if self.bot_username in text:
                new_text: str = text.replace(self.bot_username, "").replace("@", "").strip()
                response: str = self.handle_response(new_text, chat_id)
            else:
                return
        else:
            response: str = self.handle_response(text, chat_id)
        
        await update.message.reply_text(response)
    
    def handle_response(self, text: str, chat_id: int) -> str:
        return self.get_model(chat_id).discuss(text)
    
    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.logger.error(f"Update {update} caused error: {context.error}")
        await update.message.reply_text("Your message caused error, try to start again with /start command")

    def log_update(self, update: Update):
        self.logger.info(f"update from {update.effective_user.name} ({update.message.chat_id}): {update.message.text}")
