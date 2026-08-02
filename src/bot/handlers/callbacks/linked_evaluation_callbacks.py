from telegram import Update
from telegram.ext import ContextTypes


async def callback_linked_evaluation(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    avaliacao_vinculada = query.data.removeprefix(
        "vinculada:"
    )

    context.user_data["avaliacao"][
        "avaliacao_vinculada"
    ] = avaliacao_vinculada

    context.user_data["etapa"] = "finish"

    print("\n========== CADASTRO ==========\n")

    print(
        f"Avaliação vinculada: {avaliacao_vinculada}"
    )

    print("\n==============================\n")

    await query.edit_message_text(
        text="✅ Cadastro concluído!"
    )