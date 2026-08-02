from telegram import Update
from telegram.ext import ContextTypes


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    opcao = query.data

    await query.edit_message_text(
        f"Você escolheu: {opcao}"
    )