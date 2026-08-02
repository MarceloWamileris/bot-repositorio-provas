from telegram.ext import ApplicationBuilder, CommandHandler

from config.settings import settings
from bot.handlers.start_handler import start


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

        print("Handler /start registrado!")

        application.run_polling()