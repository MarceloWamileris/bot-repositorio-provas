from telegram import Update
from telegram.ext import ContextTypes

from bot.handlers.review_list_handler import (
    enviar_lista_revisoes,
)


async def callback_review_list(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    await query.message.delete()

    await enviar_lista_revisoes(
        update.effective_chat.id,
        context,
    )