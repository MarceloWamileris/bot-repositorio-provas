from telegram.ext import (
    ApplicationBuilder,
)

from config.settings import settings

from bot.register_handlers import (
    register_handlers,
)


class TelegramBot:

    def iniciar(self):

        application = (
            ApplicationBuilder()
            .token(settings.BOT_TOKEN)
            .build()
        )

        register_handlers(
            application,
        )

        print("Bot conectado ao Telegram!")

        application.run_polling()