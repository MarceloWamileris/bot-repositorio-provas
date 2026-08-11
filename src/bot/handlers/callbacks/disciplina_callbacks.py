from telegram import Update
from telegram.ext import ContextTypes

from data.catalogo_disciplinas import (
    CATALOGO_DISCIPLINAS,
)

from messages.select_professor import (
    MENSAGEM_PROFESSOR,
)

from bot.keyboards.teacher_keyboard import (
    teclado_professores,
)

from messages.select_turma_fac import (
    MENSAGEM_TURMA_FAC,
)

from bot.keyboards.fac_keyboard import (
    teclado_turma_fac,
)

from bot.utils.clean_messages import (
    add_clean_message,
)


async def callback_disciplina(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    codigo = query.data.removeprefix(
        "disciplina:",
    )

    periodo = context.user_data["avaliacao"]["periodo"]

    disciplinas = CATALOGO_DISCIPLINAS.get(
        periodo,
        [],
    )

    disciplina = next(
        (
            disciplina
            for disciplina in disciplinas
            if disciplina["codigo"] == codigo
        ),
        None,
    )

    if disciplina is None:
        return

    context.user_data["avaliacao"]["codigo_disciplina"] = (
        disciplina["codigo"]
    )

    context.user_data["avaliacao"]["nome_disciplina"] = (
        disciplina["nome"]
    )

    print("\n========== CADASTRO ==========\n")

    print(f"Período: {periodo}")
    print(f"Disciplina: {disciplina['codigo']}")

    print("\n==============================\n")

    # -------------------------------------------------
    # Exceção para FAC
    # -------------------------------------------------
    if disciplina["codigo"] == "1FAC":

        await query.edit_message_text(
            text=MENSAGEM_TURMA_FAC,
            reply_markup=teclado_turma_fac(),
        )

        add_clean_message(
            context,
            query.message.message_id,
        )

        return

    # -------------------------------------------------
    # Fluxo normal
    # -------------------------------------------------
    await query.edit_message_text(
        text=MENSAGEM_PROFESSOR,
        reply_markup=teclado_professores(),
    )

    add_clean_message(
        context,
        query.message.message_id,
    )