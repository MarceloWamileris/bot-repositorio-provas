import json

from pathlib import Path

from config.settings import settings


class TelegramPublicationQueueService:

    CAMINHO_JSON = (
        settings.BASE_STORAGE
        / "telegram_publications.json"
    )

    @classmethod
    def listar(cls) -> list[dict]:

        if not cls.CAMINHO_JSON.exists():

            return []

        with cls.CAMINHO_JSON.open(
            "r",
            encoding="utf-8",
        ) as arquivo:

            return json.load(arquivo)

    @classmethod
    def adicionar(
        cls,
        avaliacao: dict,
        arquivos: list[Path],
    ):

        publicacoes = cls.listar()

        publicacoes.append(
            {
                "avaliacao": avaliacao,
                "arquivos": [
                    str(arquivo)
                    for arquivo in arquivos
                ],
            }
        )

        cls.CAMINHO_JSON.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with cls.CAMINHO_JSON.open(
            "w",
            encoding="utf-8",
        ) as arquivo:

            json.dump(
                publicacoes,
                arquivo,
                ensure_ascii=False,
                indent=4,
            )

    @classmethod
    def remover(
        cls,
        indice: int,
    ):

        publicacoes = cls.listar()

        if indice < 0:
            return False

        if indice >= len(publicacoes):
            return False

        publicacoes.pop(indice)

        with cls.CAMINHO_JSON.open(
            "w",
            encoding="utf-8",
        ) as arquivo:

            json.dump(
                publicacoes,
                arquivo,
                ensure_ascii=False,
                indent=4,
            )

        return True