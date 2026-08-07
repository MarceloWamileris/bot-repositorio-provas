from telegram import Update
from telegram.ext import ContextTypes

from services.evaluation_service import (
    EvaluationService,
)

from messages.select_evaluation import (
    MENSAGEM_AVALIACAO,
)

from bot.keyboards.evaluation_keyboard import (
    evaluation_keyboard,
)

from messages.select_linked_evaluation import (
    MENSAGEM_AVALIACAO_VINCULADA,
)

from bot.keyboards.linked_evaluation_keyboard import (
    linked_evaluation_keyboard,
)


async def callback_confirm_evaluation(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    await query.answer()

    resultado = await EvaluationService.finalizar(
        update,
        context,
    )

    if resultado == "duplicado":

        await query.delete_message()

        return

    if resultado == "fila":

        await query.edit_message_text(
            text=(
                "✅ Sua prova foi enviada para análise.\n\n"
                "Após a aprovação do administrador, ela será adicionada "
                "ao acervo e publicada nos canais oficiais do projeto."
            )
        )

        return

    if resultado == "sucesso":

        await query.edit_message_text(
            text=(
                "✅ Sua prova foi enviada com sucesso!\n\n"
                "Ela já foi adicionada ao acervo."
            )
        )

        return

    await query.edit_message_text(
        text=(
            "❌ Ocorreu um erro inesperado durante o envio.\n"
            "Tente novamente."
        )
    )


async def callback_back_confirm_evaluation(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    await query.answer()

    avaliacao = context.user_data["avaliacao"]

    avaliacao["avaliacao"] = None

    context.user_data["etapa"] = "evaluation"

    await query.edit_message_text(
        text=MENSAGEM_AVALIACAO,
        reply_markup=evaluation_keyboard(),
    )


async def callback_back_confirm_linked_evaluation(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    await query.answer()

    avaliacao = context.user_data["avaliacao"]

    avaliacao["avaliacao_vinculada"] = None

    context.user_data["etapa"] = "linked_evaluation"

    await query.edit_message_text(
        text=MENSAGEM_AVALIACAO_VINCULADA,
        reply_markup=linked_evaluation_keyboard(),
    )