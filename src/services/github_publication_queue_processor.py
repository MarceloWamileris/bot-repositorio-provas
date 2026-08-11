import asyncio
import traceback

from services.github_publication_queue_service import (
    GitHubPublicationQueueService,
)

from services.github_sync_service import (
    GitHubSyncService,
)


class GitHubPublicationQueueProcessor:

    _lock = asyncio.Lock()

    @classmethod
    async def processar(cls, _context):

        # Impede duas execuções simultâneas
        if cls._lock.locked():
            return

        async with cls._lock:

            publicacoes = (
                GitHubPublicationQueueService.listar()
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

                    operacao = (
                        publicacao["operacao"]
                    )

                    sucesso = (
                        GitHubSyncService.sincronizar(
                            avaliacao,
                            operacao,
                        )
                    )

                    if not sucesso:
                        continue

                except Exception:

                    print("=" * 60)
                    print("ERRO AO SINCRONIZAR COM GITHUB")
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
                    GitHubPublicationQueueService.remover(
                        indice
                    )
                )

                if removida:

                    print("=" * 60)
                    print("SINCRONIZAÇÃO REMOVIDA DA FILA")
                    print(
                        f"Índice: {indice}"
                    )
                    print("=" * 60)