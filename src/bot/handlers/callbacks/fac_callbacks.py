from telegram import Update
from telegram.ext import ContextTypes

from messages.select_professor import (
    MENSAGEM_PROFESSOR,
)

from bot.keyboards.teacher_keyboard import (
    teclado_professores,
)

from bot.utils.clean_messages import (
    add_clean_message,
)


async def callback_fac(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    turma = query.data.removeprefix(
        "fac:",
    )

    context.user_data["avaliacao"]["turma_fac"] = (
        turma
    )

    await query.edit_message_text(
        text=MENSAGEM_PROFESSOR,
        reply_markup=teclado_professores(),
    )

    add_clean_message(
        context,
        query.message.message_id,
    )