from telegram import Update
from telegram.ext import ContextTypes

from data.catalogo_professores import (
    CATALOGO_PROFESSORES,
)

from messages.select_year import (
    MENSAGEM_ANO,
)


async def callback_teacher(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    id_professor = int(
        query.data.removeprefix(
            "professor:"
        )
    )

    professor = next(
        (
            professor
            for professor in CATALOGO_PROFESSORES
            if professor["id"] == id_professor
        ),
        None,
    )

    if professor is None:
        return

    context.user_data["avaliacao"]["id_professor"] = (
        professor["id"]
    )

    context.user_data["avaliacao"]["nome_professor"] = (
        professor["nome"]
    )

    context.user_data["etapa"] = "year"

    print("\n========== CADASTRO ==========\n")

    print(
        f"Professor: {professor['nome']}"
    )

    print("\n==============================\n")

    await query.edit_message_text(
        text=MENSAGEM_ANO,
    )