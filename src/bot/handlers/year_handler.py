from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from messages.select_year import (
    MENSAGEM_ANO,
)

from messages.select_semester import (
    MENSAGEM_SEMESTRE,
)

from bot.keyboards.year_keyboard import (
    teclado_ano,
)

from bot.keyboards.semester_keyboard import (
    teclado_semestres,
)

from bot.utils.clean_messages import (
    add_clean_message,
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

        mensagem = await update.message.reply_text(
            text=(
                "⚠️ Ano inválido.\n\n"
                f"{MENSAGEM_ANO}\n\n"
                f"São aceitos apenas anos entre 2020 e {ano_atual}."
            ),
            reply_markup=teclado_ano(),
        )

        context.user_data["mensagem_erro_ano_id"] = (
            mensagem.message_id
        )

        add_clean_message(
            context,
            mensagem.message_id,
        )

        return

    context.user_data["avaliacao"]["ano"] = int(
        ano
    )

    context.user_data["etapa"] = "semester"

    # Remove a mensagem de erro, caso exista
    erro_id = context.user_data.get(
        "mensagem_erro_ano_id"
    )

    if erro_id:

        try:

            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=erro_id,
            )

        except Exception:

            pass

        context.user_data.pop(
            "mensagem_erro_ano_id",
            None,
        )

    # Remove a mensagem "Digite o ano..."
    message_id = context.user_data.get(
        "mensagem_ano_id"
    )

    if message_id:

        try:

            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=message_id,
            )

        except Exception:

            pass

        context.user_data.pop(
            "mensagem_ano_id",
            None,
        )

    print("\n========== CADASTRO ==========\n")

    print(f"Ano: {ano}")

    print("\n==============================\n")

    mensagem = await update.message.reply_text(
        text=MENSAGEM_SEMESTRE,
        reply_markup=teclado_semestres(
            int(ano),
        ),
    )

    add_clean_message(
        context,
        mensagem.message_id,
    )