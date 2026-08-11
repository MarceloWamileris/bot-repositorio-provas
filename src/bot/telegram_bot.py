from telegram.ext import (
    ApplicationBuilder,
)

from config.settings import settings

from bot.register_handlers import (
    register_handlers,
)

from services.upload_cleanup_service import (
    UploadCleanupService,
)

from services.telegram_publication_queue_processor import (
    TelegramPublicationQueueProcessor,
)

from services.github_publication_queue_processor import (
    GitHubPublicationQueueProcessor,
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

        # --------------------------------------------------
        # Limpeza automática de uploads temporários
        # --------------------------------------------------

        application.job_queue.run_repeating(
            UploadCleanupService.limpar_expirados,
            interval=600,
            first=600,
        )

        # --------------------------------------------------
        # Processamento automático da fila do Telegram
        # --------------------------------------------------

        application.job_queue.run_repeating(
            TelegramPublicationQueueProcessor.processar,
            interval=10,
            first=2,
        )

        # --------------------------------------------------
        # Processamento automático da fila do GitHub
        # --------------------------------------------------

        application.job_queue.run_repeating(
            GitHubPublicationQueueProcessor.processar,
            interval=10,
            first=5,
        )

        print("Bot conectado ao Telegram!")

        application.run_polling()