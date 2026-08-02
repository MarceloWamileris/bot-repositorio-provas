from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config.settings import settings

from bot.handlers.start_handler import start
from bot.handlers.menu_handler import menu
from bot.handlers.file_handler import receber_arquivo


class TelegramBot:

    def iniciar(self):

        application = (
            ApplicationBuilder()
            .token(settings.BOT_TOKEN)
            .build()
        )

        application.add_handler(
            CommandHandler(
                "start",
                start,
            )
        )

        application.add_handler(
            CallbackQueryHandler(menu)
        )

        application.add_handler(
            MessageHandler(
                filters.PHOTO | filters.Document.PDF,
                receber_arquivo,
            )
        )

        print("Bot conectado ao Telegram!")

        application.run_polling()