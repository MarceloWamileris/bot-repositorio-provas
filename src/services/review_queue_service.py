from data.review_queue import REVIEW_QUEUE


class ReviewQueueService:

    @classmethod
    def adicionar(
        cls,
        usuario_id: int,
        avaliacao: dict,
        arquivos: list,
    ):

        REVIEW_QUEUE.append(
            {
                "usuario_id": usuario_id,
                "avaliacao": avaliacao.copy(),
                "arquivos": arquivos.copy(),
            }
        )

        print("\n========== FILA DE REVISÃO ==========\n")

        print(REVIEW_QUEUE)

        print("\n=====================================\n")