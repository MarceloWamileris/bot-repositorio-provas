from telegram import Update
from telegram.ext import ContextTypes

from services.duplicate_service import (
    DuplicateService,
)
from services.storage_service import (
    StorageService,
)
from services.review_service import (
    ReviewService,
)


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

            await ReviewService.iniciar(
                update,
                context,
                avaliacao,
            )

            return "duplicado"

        for arquivo in arquivos:

            destino = StorageService.armazenar_arquivo(
                avaliacao,
                arquivo["caminho"],
            )

            print(
                f"Arquivo armazenado em: {destino}"
            )

        return "armazenado"