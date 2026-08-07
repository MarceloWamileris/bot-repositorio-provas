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
        tipo: str = "nova",
        acervo: dict | None = None,
    ):

        REVIEW_QUEUE.append(
            {
                "tipo": tipo,
                "usuario_id": usuario_id,
                "avaliacao": avaliacao.copy(),
                "arquivos": arquivos.copy(),
                "acervo": (
                    acervo.copy()
                    if acervo is not None
                    else None
                ),
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
    def listar(cls):

        grupos = {}

        for indice, revisao in enumerate(REVIEW_QUEUE):

            avaliacao = revisao["avaliacao"]

            chave = (
                avaliacao["codigo_disciplina"],
                avaliacao["id_professor"],
                avaliacao["ano"],
                avaliacao["semestre"],
                avaliacao["turno"],
                avaliacao["avaliacao"],
            )

            submissao = revisao.copy()
            submissao["review_queue_index"] = indice

            if chave not in grupos:

                grupos[chave] = {
                    "indice": indice,
                    "tipo": revisao.get(
                        "tipo",
                        "nova",
                    ),
                    "acervo": revisao.get(
                        "acervo",
                    ),
                    "avaliacao": avaliacao,
                    "quantidade": 1,
                    "submissoes": [submissao],
                }

            else:

                grupos[chave]["quantidade"] += 1
                grupos[chave]["submissoes"].append(
                    submissao
                )

        return list(grupos.values())

    @classmethod
    def obter(
        cls,
        indice: int,
    ):

        if indice < 0 or indice >= len(REVIEW_QUEUE):
            return None

        return REVIEW_QUEUE[indice]

    @classmethod
    def remover_submissao(
        cls,
        review_index: int,
        submission_index: int,
    ):

        grupos = cls.listar()

        print("\n========== GRUPOS ANTES ==========")
        pprint(grupos)
        print("==================================")

        grupo_atual = next(
            (
                grupo
                for grupo in grupos
                if grupo["indice"] == review_index
            ),
            None,
        )

        if grupo_atual is None:
            print("Grupo atual não encontrado.")
            return False

        chave = (
            grupo_atual["avaliacao"]["codigo_disciplina"],
            grupo_atual["avaliacao"]["id_professor"],
            grupo_atual["avaliacao"]["ano"],
            grupo_atual["avaliacao"]["semestre"],
            grupo_atual["avaliacao"]["turno"],
            grupo_atual["avaliacao"]["avaliacao"],
        )

        grupos = cls.listar()

        grupo = next(
            (
                g
                for g in grupos
                if (
                    g["avaliacao"]["codigo_disciplina"],
                    g["avaliacao"]["id_professor"],
                    g["avaliacao"]["ano"],
                    g["avaliacao"]["semestre"],
                    g["avaliacao"]["turno"],
                    g["avaliacao"]["avaliacao"],
                )
                == chave
            ),
            None,
        )

        if grupo is None:
            print("Grupo pela chave não encontrado.")
            return False

        if submission_index >= len(grupo["submissoes"]):
            print("Índice da submissão inválido.")
            return False

        submissao = grupo["submissoes"][submission_index]

        print("\n========== FILA ANTES DO POP ==========")
        pprint(REVIEW_QUEUE)
        print("=======================================")

        print(
            f"\nRemovendo review_queue_index = "
            f"{submissao['review_queue_index']}"
        )

        REVIEW_QUEUE.pop(
            submissao["review_queue_index"]
        )

        print("\n========== FILA DEPOIS DO POP ==========")
        pprint(REVIEW_QUEUE)
        print("========================================")

        ReviewQueueStorageService.salvar()

        print("\n========== GRUPOS DEPOIS ==========")
        pprint(cls.listar())
        print("===================================")

        return True

    @classmethod
    def remover_revisao(
        cls,
        review_index: int,
    ):

        grupos = cls.listar()

        grupo = next(
            (
                revisao
                for revisao in grupos
                if revisao["indice"] == review_index
            ),
            None,
        )

        if grupo is None:
            return False

        indices = sorted(
            (
                submissao["review_queue_index"]
                for submissao in grupo["submissoes"]
            ),
            reverse=True,
        )

        for indice in indices:
            REVIEW_QUEUE.pop(indice)

        ReviewQueueStorageService.salvar()

        return True