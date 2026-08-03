from telegram import Update
from telegram.ext import ContextTypes

from messages.select_linked_evaluation import (
    MENSAGEM_AVALIACAO_VINCULADA,
)

from bot.keyboards.linked_evaluation_keyboard import (
    linked_evaluation_keyboard,
)

from services.evaluation_service import (
    EvaluationService,
)


async def callback_evaluation(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    avaliacao = query.data.removeprefix(
        "avaliacao:"
    )

    context.user_data["avaliacao"][
        "avaliacao"
    ] = avaliacao

    print("\n========== CADASTRO ==========\n")

    print(f"Avaliação: {avaliacao}")

    print("\n==============================\n")

    if avaliacao == "AVS":

        context.user_data["etapa"] = (
            "linked_evaluation"
        )

        await query.edit_message_text(
            text=MENSAGEM_AVALIACAO_VINCULADA,
            reply_markup=linked_evaluation_keyboard(),
        )

        return

    context.user_data["etapa"] = "finish"

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