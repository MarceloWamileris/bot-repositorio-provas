from telegram import Update
from telegram.ext import ContextTypes

from services.review_queue_service import (
    ReviewQueueService,
)
from services.session_service import (
    SessionService,
)


async def callback_review_request(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    ReviewQueueService.adicionar(
        usuario_id=update.effective_user.id,
        avaliacao=context.user_data["avaliacao"],
        arquivos=context.user_data["arquivos"],
        tipo="comparacao",
        acervo=context.user_data["prova_acervo"],
    )

    context.user_data.pop(
        "prova_acervo",
        None,
    )

    SessionService.finalizar(
        context,
    )

    await query.edit_message_text(
        text=(
            "✅ Sua solicitação foi enviada para análise.\n\n"
            "O administrador comparará a prova que atualmente "
            "está no acervo com a versão que você enviou e "
            "decidirá qual das duas será mantida no acervo."
        )
    )


async def callback_review_cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    context.user_data.pop(
        "prova_acervo",
        None,
    )

    SessionService.finalizar(
        context,
    )

    await query.edit_message_text(
        text=(
            "❌ Envio cancelado.\n\n"
            "A prova não foi encaminhada para análise."
        )
    )