from telegram import Update
from telegram.ext import ContextTypes

from messages.upload import MENSAGEM_UPLOAD
from bot.keyboards.finish_keyboard import teclado_finalizar
from services.file_service import FileService


async def upload(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    context.user_data["arquivos"] = []

    context.user_data["pasta_envio"] = (
        FileService.criar_pasta_envio(
            update.effective_user.id
        )
    )

    mensagem = await query.edit_message_text(
        text=MENSAGEM_UPLOAD.format(total=0),
        reply_markup=teclado_finalizar(),
    )

    context.user_data["mensagem_upload_id"] = (
        mensagem.message_id
    )