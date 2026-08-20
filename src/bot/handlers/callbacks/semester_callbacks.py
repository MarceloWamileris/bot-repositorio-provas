from telegram import Update
from telegram.ext import ContextTypes

from messages.select_shift import (
    MENSAGEM_TURNO,
)

from bot.keyboards.shift_keyboard import (
    shift_keyboard,
)

from bot.utils.clean_messages import (
    add_clean_message,
)


async def callback_semester(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    semestre = int(
        query.data.removeprefix(
            "semestre:"
        )
    )

    context.user_data["avaliacao"]["semestre"] = (
        semestre
    )

    context.user_data["etapa"] = "shift"

    await query.edit_message_text(
        text=MENSAGEM_TURNO,
        reply_markup=shift_keyboard(),
    )

    add_clean_message(
        context,
        query.message.message_id,
    )