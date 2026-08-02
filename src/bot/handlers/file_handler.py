from telegram import Update
from telegram.ext import ContextTypes

from messages.upload import MENSAGEM_UPLOAD
from bot.keyboards.finish_keyboard import teclado_finalizar
from services.file_service import FileService


async def receber_arquivo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if "arquivos" not in context.user_data:
        context.user_data["arquivos"] = []

    if update.message.document:
        arquivo = update.message.document

        pasta_usuario = FileService.criar_pasta_usuario(
            update.effective_user.id
        )

        telegram_file = await arquivo.get_file()

        caminho = pasta_usuario / arquivo.file_name

        await telegram_file.download_to_drive(caminho)

        context.user_data["arquivos"].append(
            {
                "tipo": "pdf",
                "file_id": arquivo.file_id,
                "nome": arquivo.file_name,
                "caminho": str(caminho),
            }
        )

    elif update.message.photo:
        foto = update.message.photo[-1]

        context.user_data["arquivos"].append(
            {
                "tipo": "imagem",
                "file_id": foto.file_id,
            }
        )

    quantidade = len(context.user_data["arquivos"])

    message_id = context.user_data.get("contador_msg_id")

    if message_id:
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=message_id,
            text=MENSAGEM_UPLOAD.format(total=quantidade),
            reply_markup=teclado_finalizar(),
        )