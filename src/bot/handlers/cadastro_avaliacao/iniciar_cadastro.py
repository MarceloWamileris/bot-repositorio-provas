from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards.period_keyboard import teclado_periodos
from messages.select_period import MENSAGEM_PERIODO

from bot.utils.clean_messages import (
    add_clean_message,
)


async def iniciar_cadastro(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    context.user_data["avaliacao"] = {}

    mensagem_origem = (
        update.message
        if update.message
        else update.callback_query.message
    )

    mensagem_enviada = await mensagem_origem.reply_text(
        text=MENSAGEM_PERIODO,
        reply_markup=teclado_periodos(),
    )

    add_clean_message(
        context,
        mensagem_enviada.message_id,
    )