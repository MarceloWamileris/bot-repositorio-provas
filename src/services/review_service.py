from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards.review_keyboard import (
    review_keyboard,
)


class ReviewService:

    @classmethod
    async def iniciar(
        cls,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        avaliacao: dict,
        prova_acervo: dict,
    ):

        if prova_acervo is None:
            return

        # Salva a prova atual do acervo para ser utilizada
        # caso o usuário solicite a revisão.
        context.user_data["prova_acervo"] = (
            prova_acervo
        )

        paginas = prova_acervo["paginas"]

        for pagina in paginas:

            with pagina.open("rb") as arquivo:

                if pagina.suffix.lower() == ".pdf":

                    await context.bot.send_document(
                        chat_id=update.effective_chat.id,
                        document=arquivo,
                    )

                else:

                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=arquivo,
                    )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                "⚠️ Esta avaliação já existe no acervo.\n\n"
                "Compare os arquivos acima com a prova que você acabou de enviar.\n\n"
                "Se a sua versão estiver mais nítida ou mais completa, "
                "você pode solicitar uma revisão. "
                "O administrador analisará ambas as versões e decidirá "
                "se a prova atual deverá ser substituída."
            ),
            reply_markup=review_keyboard(),
        )