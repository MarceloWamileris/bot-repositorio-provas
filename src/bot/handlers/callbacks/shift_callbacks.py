from telegram import Update
from telegram.ext import ContextTypes

from messages.select_evaluation import MENSAGEM_AVALIACAO

from bot.keyboards.evaluation_keyboard import (
    evaluation_keyboard,
)

from bot.utils.clean_messages import (
    add_clean_message,
)


async def callback_shift(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    turno = query.data.removeprefix(
        "turno:"
    )

    context.user_data["avaliacao"]["turno"] = turno

    context.user_data["etapa"] = "evaluation"

    await query.edit_message_text(
        text=MENSAGEM_AVALIACAO,
        reply_markup=evaluation_keyboard(),
    )

    add_clean_message(
        context,
        query.message.message_id,
    )