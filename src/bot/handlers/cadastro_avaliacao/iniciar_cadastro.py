from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards.period_keyboard import teclado_periodos
from messages.select_period import MENSAGEM_PERIODO


async def iniciar_cadastro(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    context.user_data["avaliacao"] = {}

    mensagem = (
        update.message
        if update.message
        else update.callback_query.message
    )

    await mensagem.reply_text(
        text=MENSAGEM_PERIODO,
        reply_markup=teclado_periodos(),
    )