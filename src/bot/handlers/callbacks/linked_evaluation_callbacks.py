from telegram import Update
from telegram.ext import ContextTypes

from messages.confirm_evaluation import (
    MENSAGEM_CONFIRMACAO,
)

from bot.keyboards.confirm_evaluation_keyboard import (
    confirm_evaluation_keyboard,
)

from bot.utils.clean_messages import (
    add_clean_message,
)


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

    context.user_data["etapa"] = (
        "confirm_evaluation"
    )

    dados = context.user_data["avaliacao"]

    turma = ""

    if dados.get("turma_fac"):

        turma = (
            f"Turma: {dados['turma_fac']}\n"
        )

    await query.edit_message_text(
        text=MENSAGEM_CONFIRMACAO.format(
            disciplina=dados["codigo_disciplina"],
            turma=turma,
            professor=dados["nome_professor"],
            ano=dados["ano"],
            semestre=dados["semestre"],
            turno=dados["turno"],
            avaliacao=dados["avaliacao"],
            avaliacao_vinculada=(
                f"Avaliação vinculada: "
                f"{dados['avaliacao_vinculada']}"
            ),
        ),
        reply_markup=confirm_evaluation_keyboard(
            is_avs=True,
        ),
    )

    add_clean_message(
        context,
        query.message.message_id,
    )