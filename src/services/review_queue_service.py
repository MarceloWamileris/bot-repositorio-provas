from pprint import pprint

from data.review_queue import REVIEW_QUEUE

from services.review_queue_storage_service import (
    ReviewQueueStorageService,
)


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

        ReviewQueueStorageService.salvar()

        print("\n===== SUBMISSÃO ADICIONADA =====")

        pprint(
            REVIEW_QUEUE[-1]
        )

        print("===============================\n")

        print("\n========== FILA DE REVISÃO ==========\n")

        print(
            f"Revisões pendentes: {len(REVIEW_QUEUE)}"
        )

        print("\n=====================================\n")

    @classmethod
    def listar(
        cls,
    ):

        grupos = {}

        for indice, revisao in enumerate(
            REVIEW_QUEUE,
        ):

            avaliacao = revisao["avaliacao"]

            chave = (
                avaliacao["codigo_disciplina"],
                avaliacao["id_professor"],
                avaliacao["ano"],
                avaliacao["semestre"],
                avaliacao["turno"],
                avaliacao["avaliacao"],
            )

            if chave not in grupos:

                grupos[chave] = {
                    "indice": indice,
                    "avaliacao": avaliacao,
                    "quantidade": 1,
                    "submissoes": [revisao],
                }

            else:

                grupos[chave]["quantidade"] += 1

                grupos[chave]["submissoes"].append(
                    revisao
                )

        return list(
            grupos.values()
        )