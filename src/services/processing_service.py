from telegram import Update
from telegram.ext import ContextTypes

from data.modelo_avaliacao import nova_avaliacao

from bot.handlers.cadastro_avaliacao.iniciar_cadastro import (
    iniciar_cadastro,
)

from services.ocr_service import OCRService


class ProcessingService:

    @classmethod
    async def iniciar_processamento(
        cls,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        arquivos = context.user_data.get(
            "arquivos",
            [],
        )

        for arquivo in arquivos:

            await OCRService.extrair_texto(
                arquivo["caminho"],
            )

        context.user_data["avaliacao"] = nova_avaliacao()

        await iniciar_cadastro(
            update,
            context,
        )