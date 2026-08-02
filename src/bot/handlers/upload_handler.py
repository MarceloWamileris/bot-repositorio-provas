from telegram import Update
from telegram.ext import ContextTypes

from messages.upload import MENSAGEM_UPLOAD


async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.edit_message_text(
        MENSAGEM_UPLOAD,
    )