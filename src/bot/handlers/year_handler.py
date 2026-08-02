from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from messages.select_year import MENSAGEM_ANO
from messages.select_semester import MENSAGEM_SEMESTRE

from bot.keyboards.semester_keyboard import (
    teclado_semestres,
)


async def receber_ano(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if context.user_data.get("etapa") != "year":
        return

    ano = update.message.text.strip()

    ano_atual = datetime.now().year

    if (
        not ano.isdigit()
        or len(ano) != 4
        or not (2020 <= int(ano) <= ano_atual)
    ):

        await update.message.reply_text(
            text=(
                "⚠️ Ano inválido.\n\n"
                f"{MENSAGEM_ANO}\n\n"
                f"São aceitos apenas anos entre 2020 e {ano_atual}."
            )
        )

        return

    context.user_data["avaliacao"]["ano"] = int(ano)

    context.user_data["etapa"] = "semester"

    print("\n========== CADASTRO ==========\n")

    print(f"Ano: {ano}")

    print("\n==============================\n")

    await update.message.reply_text(
        text=MENSAGEM_SEMESTRE,
        reply_markup=teclado_semestres(
            int(ano),
        ),
    )