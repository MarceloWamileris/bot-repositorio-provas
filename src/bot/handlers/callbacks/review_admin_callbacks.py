from telegram import Update
from telegram.ext import ContextTypes

from services.review_queue_service import (
    ReviewQueueService,
)

from bot.keyboards.review_details_keyboard import (
    review_details_keyboard,
)


async def callback_review_details(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    indice = int(
        query.data.removeprefix(
            "review:"
        )
    )

    revisoes = ReviewQueueService.listar()

    grupo = next(
        (
            revisao
            for revisao in revisoes
            if revisao["indice"] == indice
        ),
        None,
    )

    if grupo is None:

        await query.edit_message_text(
            text=(
                "⚠️ Esta revisão não está mais disponível."
            )
        )

        return

    avaliacao = grupo["avaliacao"]

    await query.edit_message_text(
        text=(
            "📄 Revisão selecionada\n\n"
            f"Disciplina: {avaliacao['codigo_disciplina']}\n"
            f"Professor: {avaliacao['nome_professor']}\n"
            f"Ano: {avaliacao['ano']}\n"
            f"Semestre: {avaliacao['semestre']}\n"
            f"Turno: {avaliacao['turno']}\n"
            f"Avaliação: {avaliacao['avaliacao']}\n\n"
            f"Versões pendentes: {grupo['quantidade']}\n\n"
            "⬇️ Selecione uma versão:"
        ),
        reply_markup=review_details_keyboard(
            grupo,
        ),
    )