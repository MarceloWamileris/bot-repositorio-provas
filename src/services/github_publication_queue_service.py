import json

from pathlib import Path

from config.settings import settings


class GitHubPublicationQueueService:

    CAMINHO_JSON = (
        settings.BASE_STORAGE
        / "github_publications.json"
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
        operacao: str,
    ):

        if operacao not in (
            "adicionar",
            "substituir",
        ):

            raise ValueError(
                f"Operação inválida: {operacao}"
            )

        publicacoes = cls.listar()

        publicacoes.append(
            {
                "avaliacao": avaliacao,
                "operacao": operacao,
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