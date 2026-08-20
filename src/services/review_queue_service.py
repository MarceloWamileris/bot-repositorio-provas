import logging

from data.review_queue import REVIEW_QUEUE

from services.review_queue_storage_service import (
    ReviewQueueStorageService,
)

logger = logging.getLogger(__name__)


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

        logger.info(
            f"Submissão adicionada à fila de revisão "
            f"(revisões pendentes: {len(REVIEW_QUEUE)})"
        )

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

        grupo_atual = next(
            (
                grupo
                for grupo in grupos
                if grupo["indice"] == review_index
            ),
            None,
        )

        if grupo_atual is None:
            logger.warning(
                "remover_submissao: grupo atual não "
                "encontrado na fila de revisão."
            )
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
            logger.warning(
                "remover_submissao: grupo pela chave "
                "não encontrado."
            )
            return False

        if submission_index >= len(grupo["submissoes"]):
            logger.warning(
                "remover_submissao: índice da "
                "submissão inválido "
                f"({submission_index})."
            )
            return False

        submissao = grupo["submissoes"][submission_index]

        REVIEW_QUEUE.pop(
            submissao["review_queue_index"]
        )

        ReviewQueueStorageService.salvar()

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