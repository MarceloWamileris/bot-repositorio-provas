from telegram import Update
from telegram.ext import ContextTypes

from services.duplicate_service import DuplicateService
from services.storage_service import StorageService


class EvaluationService:

    @classmethod
    async def finalizar(
        cls,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        avaliacao = context.user_data["avaliacao"]

        arquivos = context.user_data.get(
            "arquivos",
            [],
        )

        if DuplicateService.existe(
            avaliacao,
        ):

            print(
                "Avaliação já existe no acervo."
            )

            return

        for arquivo in arquivos:

            destino = StorageService.armazenar_arquivo(
                avaliacao,
                arquivo["caminho"],
            )

            print(
                f"Arquivo armazenado em: {destino}"
            )