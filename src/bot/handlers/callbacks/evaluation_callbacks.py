from telegram import Update
from telegram.ext import ContextTypes

from messages.select_linked_evaluation import (
    MENSAGEM_AVALIACAO_VINCULADA,
)

from messages.confirm_evaluation import (
    MENSAGEM_CONFIRMACAO,
)

from bot.keyboards.linked_evaluation_keyboard import (
    linked_evaluation_keyboard,
)

from bot.keyboards.confirm_evaluation_keyboard import (
    confirm_evaluation_keyboard,
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

    # -------------------------------------------------
    # Fluxo AVS
    # -------------------------------------------------
    if avaliacao == "AVS":

        context.user_data["etapa"] = (
            "linked_evaluation"
        )

        await query.edit_message_text(
            text=MENSAGEM_AVALIACAO_VINCULADA,
            reply_markup=linked_evaluation_keyboard(),
        )

        return

    # -------------------------------------------------
    # Tela de confirmação
    # -------------------------------------------------
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
            avaliacao_vinculada="",
        ),
        reply_markup=confirm_evaluation_keyboard(
            is_avs=False,
        ),
    )