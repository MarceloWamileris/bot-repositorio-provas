from telegram import Update
from telegram.ext import ContextTypes

from bot.handlers.callbacks.menu_callbacks import (
    callback_enviar,
    callback_consultar,
    callback_ajuda,
)

from bot.handlers.upload_handler import upload

from bot.handlers.callbacks.finish_callbacks import (
    callback_finalizar,
)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    opcao = query.data

    if opcao == "enviar":
        await callback_enviar(update, context)

    elif opcao == "consultar":
        await callback_consultar(update, context)

    elif opcao == "ajuda":
        await callback_ajuda(update, context)

    elif opcao == "upload":
        await upload(update, context)

    elif opcao == "finalizar_envio":
        await callback_finalizar(update, context)