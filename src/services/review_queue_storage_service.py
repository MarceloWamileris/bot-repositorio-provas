import json
from pathlib import Path

from data.review_queue import REVIEW_QUEUE


class ReviewQueueStorageService:

    ARQUIVO = Path(
        "src/data/review_queue.json"
    )

    @classmethod
    def carregar(
        cls,
    ):

        if not cls.ARQUIVO.exists():

            return

        with open(
            cls.ARQUIVO,
            "r",
            encoding="utf-8",
        ) as arquivo:

            dados = json.load(
                arquivo
            )

        for revisao in dados:

            for arquivo in revisao["arquivos"]:

                arquivo["caminho"] = Path(
                    arquivo["caminho"]
                )

        REVIEW_QUEUE.clear()

        REVIEW_QUEUE.extend(
            dados
        )

    @classmethod
    def salvar(
        cls,
    ):

        dados = []

        for revisao in REVIEW_QUEUE:

            revisao_json = {
                "usuario_id": revisao["usuario_id"],
                "avaliacao": revisao["avaliacao"].copy(),
                "arquivos": [],
            }

            for arquivo in revisao["arquivos"]:

                revisao_json["arquivos"].append(
                    {
                        "tipo": arquivo["tipo"],
                        "file_id": arquivo["file_id"],
                        "nome": arquivo["nome"],
                        "caminho": str(
                            arquivo["caminho"]
                        ),
                    }
                )

            dados.append(
                revisao_json
            )

        with open(
            cls.ARQUIVO,
            "w",
            encoding="utf-8",
        ) as arquivo:

            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=4,
            )

    @classmethod
    def limpar(
        cls,
    ):

        REVIEW_QUEUE.clear()

        cls.salvar()