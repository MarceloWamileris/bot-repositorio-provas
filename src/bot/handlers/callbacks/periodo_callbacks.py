from telegram import Update
from telegram.ext import ContextTypes

from messages.select_disciplina import (
    MENSAGEM_DISCIPLINA,
)

from bot.keyboards.disciplina_keyboard import (
    teclado_disciplinas,
)

from bot.utils.clean_messages import (
    add_clean_message,
)


async def callback_periodo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    periodo = query.data.removeprefix(
        "periodo:",
    )

    context.user_data["avaliacao"]["periodo"] = (
        periodo
    )

    mensagem = await query.edit_message_text(
        text=MENSAGEM_DISCIPLINA,
        reply_markup=teclado_disciplinas(
            periodo,
        ),
    )

    add_clean_message(
        context,
        mensagem.message_id,
    )