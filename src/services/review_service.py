from telegram import Update
from telegram.ext import ContextTypes

from services.telegram_service import (
    TelegramService,
)

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

        context.user_data["prova_acervo"] = (
            prova_acervo
        )

        paginas = prova_acervo["paginas"]

        for pagina in paginas:

            with pagina.open("rb") as arquivo:

                if pagina.suffix.lower() == ".pdf":

                    await TelegramService.send_document(
                        bot=context.bot,
                        chat_id=update.effective_chat.id,
                        document=arquivo,
                    )

                else:

                    await TelegramService.send_photo(
                        bot=context.bot,
                        chat_id=update.effective_chat.id,
                        photo=arquivo,
                    )

        await TelegramService.send_message(
            bot=context.bot,
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