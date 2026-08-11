import asyncio
import traceback
from pathlib import Path

from services.telegram_publication_queue_service import (
    TelegramPublicationQueueService,
)

from services.telegram_publication_service import (
    TelegramPublicationService,
)


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

                    print("=" * 60)
                    print("ERRO AO PUBLICAR AVALIAÇÃO")
                    print(
                        f"Índice da publicação: "
                        f"{indice}"
                    )
                    print("=" * 60)

                    traceback.print_exc()

                    # Mantém a publicação no JSON
                    # para uma próxima tentativa.
                    continue

                removida = (
                    TelegramPublicationQueueService.remover(
                        indice
                    )
                )

                if removida:

                    print("=" * 60)
                    print("PUBLICAÇÃO REMOVIDA DA FILA")
                    print(
                        f"Índice: {indice}"
                    )
                    print("=" * 60)
