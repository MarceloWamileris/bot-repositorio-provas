from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)

from config.settings import settings
from bot.handlers.start_handler import start
from bot.handlers.menu_handler import menu


class TelegramBot:
    def iniciar(self):
        application = (
            ApplicationBuilder()
            .token(settings.BOT_TOKEN)
            .build()
        )

        application.add_handler(
            CommandHandler("start", start)
        )

        application.add_handler(
            CallbackQueryHandler(menu)
        )

        print("Bot conectado ao Telegram!")

        application.run_polling()