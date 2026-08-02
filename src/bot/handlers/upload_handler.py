from telegram import Update
from telegram.ext import ContextTypes

from messages.upload import MENSAGEM_UPLOAD
from bot.keyboards.finish_keyboard import teclado_finalizar


async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    mensagem = await query.edit_message_text(
        text=MENSAGEM_UPLOAD.format(total=0),
        reply_markup=teclado_finalizar(),
    )

    context.user_data["contador_msg_id"] = mensagem.message_id