from telegram import Update
from telegram.ext import ContextTypes

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

        print("\n========== PROCESSAMENTO ==========\n")

        print(f"Usuário: {update.effective_user.id}")
        print(f"Arquivos recebidos: {len(arquivos)}\n")

        for indice, arquivo in enumerate(arquivos, start=1):

            print(f"[{indice}] {arquivo['nome']}")

            if arquivo["tipo"] == "pdf":

                print("→ PDF identificado.")

            elif arquivo["tipo"] == "imagem":

                print("→ Imagem identificada.")

            await OCRService.extrair_texto(
                arquivo["caminho"],
            )

            print()

        print("==================================\n")