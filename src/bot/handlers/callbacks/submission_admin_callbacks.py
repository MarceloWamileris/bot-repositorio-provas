from telegram import Update
from telegram.ext import ContextTypes

from services.review_queue_service import (
    ReviewQueueService,
)

from bot.keyboards.submission_details_keyboard import (
    submission_details_keyboard,
)


async def callback_submission_details(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    _, review_index, submission_index = (
        query.data.split(":")
    )

    review_index = int(
        review_index
    )

    submission_index = int(
        submission_index
    )

    revisoes = ReviewQueueService.listar()

    grupo = next(
        (
            revisao
            for revisao in revisoes
            if revisao["indice"] == review_index
        ),
        None,
    )

    if grupo is None:

        await query.edit_message_text(
            "⚠️ Esta revisão não está mais disponível."
        )

        return

    submissao = grupo["submissoes"][
        submission_index
    ]

    await query.edit_message_text(
        text=(
            f"📄 Versão {submission_index + 1}\n\n"
            f"Usuário: {submissao['usuario_id']}\n"
            f"Arquivos enviados: {len(submissao['arquivos'])}"
        ),
        reply_markup=submission_details_keyboard(
            review_index,
        ),
    )