import asyncio
import logging
from pathlib import Path

from services.telegram_publication_queue_service import (
    TelegramPublicationQueueService,
)

from services.telegram_publication_service import (
    TelegramPublicationService,
)

logger = logging.getLogger(__name__)


class TelegramPublicationQueueProcessor:

    _lock = asyncio.Lock()

    @classmethod
    async def processar(cls, _context):

        # Impede duas execuções simultâneas
        if cls._lock.locked():
            return

        async with cls._lock:

            publicacoes = (
                TelegramPublicationQueueService.listar()
            )

            if not publicacoes:
                return

            # Processa do último para o primeiro.
            # Assim, remover uma publicação não altera
            # os índices das publicações que ainda serão processadas.
            for indice in range(
                len(publicacoes) - 1,
                -1,
                -1,
            ):

                publicacao = publicacoes[indice]

                try:

                    avaliacao = (
                        publicacao["avaliacao"]
                    )

                    arquivos = [
                        Path(caminho)
                        for caminho in publicacao["arquivos"]
                    ]

                    await (
                        TelegramPublicationService.publicar_prova(
                            avaliacao,
                            arquivos,
                        )
                    )

                except Exception:

                    logger.error(
                        f"Erro ao publicar avaliação no "
                        f"Telegram (índice: {indice})",
                        exc_info=True,
                    )

                    # Mantém a publicação no JSON
                    # para uma próxima tentativa.
                    continue

                removida = (
                    TelegramPublicationQueueService.remover(
                        indice
                    )
                )

                if removida:

                    logger.info(
                        f"Publicação removida da fila "
                        f"(índice: {indice})"
                    )