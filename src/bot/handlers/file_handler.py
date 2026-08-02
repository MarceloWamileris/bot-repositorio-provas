from telegram import Update
from telegram.ext import ContextTypes

from messages.upload import MENSAGEM_UPLOAD
from bot.keyboards.finish_keyboard import teclado_finalizar


async def receber_arquivo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if "arquivos" not in context.user_data:
        context.user_data["arquivos"] = []

    pasta_envio = context.user_data["pasta_envio"]

    if update.message.document:
        arquivo = update.message.document

        telegram_file = await arquivo.get_file()

        quantidade_pdfs = sum(
            1
            for arquivo_salvo in context.user_data["arquivos"]
            if arquivo_salvo["tipo"] == "pdf"
        )

        nome_arquivo = f"pdf_{quantidade_pdfs + 1}.pdf"

        caminho = pasta_envio / nome_arquivo

        await telegram_file.download_to_drive(caminho)

        context.user_data["arquivos"].append(
            {
                "tipo": "pdf",
                "file_id": arquivo.file_id,
                "nome": nome_arquivo,
                "caminho": str(caminho),
            }
        )

    elif update.message.photo:
        foto = update.message.photo[-1]

        telegram_file = await foto.get_file()

        quantidade_imagens = sum(
            1
            for arquivo_salvo in context.user_data["arquivos"]
            if arquivo_salvo["tipo"] == "imagem"
        )

        nome_arquivo = f"pagina_{quantidade_imagens + 1}.jpg"

        caminho = pasta_envio / nome_arquivo

        await telegram_file.download_to_drive(caminho)

        context.user_data["arquivos"].append(
            {
                "tipo": "imagem",
                "file_id": foto.file_id,
                "nome": nome_arquivo,
                "caminho": str(caminho),
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