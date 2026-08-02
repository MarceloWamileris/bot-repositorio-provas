from telegram import Update
from telegram.ext import ContextTypes

from messages.envio import MENSAGEM_INSTRUCOES
from bot.keyboards.upload_keyboard import teclado_instrucoes


async def callback_enviar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    # Limpa qualquer envio anterior
    context.user_data["arquivos"] = []
    context.user_data.pop("contador_msg_id", None)

    await query.edit_message_text(
        text=MENSAGEM_INSTRUCOES,
        reply_markup=teclado_instrucoes(),
    )


async def callback_consultar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        "📚 Você escolheu consultar o acervo."
    )


async def callback_ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        "❓ Você escolheu ajuda."
    )