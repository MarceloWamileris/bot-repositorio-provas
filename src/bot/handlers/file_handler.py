from pathlib import Path

import logging

from telegram import Update
from telegram.ext import ContextTypes

from messages.upload import MENSAGEM_UPLOAD

from bot.keyboards.finish_keyboard import (
    teclado_finalizar,
)

from bot.utils.validar_assinatura import validar_assinatura

from bot.utils.clean_messages import (
    add_clean_message,
)

logger = logging.getLogger(__name__)


EXTENSOES_PERMITIDAS = {
    ".pdf",
#    ".txt",
#    ".docx",
    ".png",
    ".jpg",
    ".jpeg",
#    ".heic",
#    ".webp",
}

MAX_ARQUIVOS = 10

MAX_TAMANHO_MB = 20

MAX_TAMANHO_BYTES = (
    MAX_TAMANHO_MB * 1024 * 1024
)


async def receber_arquivo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if context.user_data.get("etapa") != "upload":

        await update.message.reply_text(
            text=(
                "📄 Não há nenhum envio em andamento.\n\n"
                "Para iniciar uma nova avaliação, utilize o comando:\n\n"
                "/start"
            ),
        )

        return

    # Impede envio de álbuns (media groups)
    if update.message.media_group_id:

        ultimo_media_group = context.user_data.get(
            "ultimo_media_group"
        )

        if (
            ultimo_media_group
            != update.message.media_group_id
        ):

            context.user_data["ultimo_media_group"] = (
                update.message.media_group_id
            )

            await update.message.reply_text(
                text=(
                    "⚠️ Envie apenas um arquivo por vez, respeitando a ordem da prova.\n\n"
                    "Após cada envio, envie o próximo arquivo ou clique em "
                    '"✅ Finalizar envio" somente quando tiver enviado toda a prova.'
                )
            )

        return

    if "arquivos" not in context.user_data:

        context.user_data["arquivos"] = []

    pasta_envio = context.user_data["pasta_envio"]

    # ------------------------
    # Limite de quantidade
    # ------------------------
    if len(context.user_data["arquivos"]) >= MAX_ARQUIVOS:

        await update.message.reply_text(
            text=(
                f"❌ Você atingiu o limite de {MAX_ARQUIVOS} arquivos por envio.\n\n"
                "Se sua avaliação possuir muitas páginas, prefira agrupá-las em um único PDF."
            ),
        )

        return

    # ------------------------
    # Variáveis que serão preenchidas
    # tanto pelo caminho "documento"
    # quanto pelo caminho "foto"
    # ------------------------
    telegram_file = None
    extensao = None
    tipo = None
    prefixo = None
    file_id = None

    if update.message.document:

        arquivo = update.message.document

        # Nome original enviado pelo usuário
        nome_original = (
            arquivo.file_name or ""
        )

        # Extensão do arquivo
        extensao = (
            Path(nome_original)
            .suffix
            .lower()
        )

        # Validação das extensões
        if extensao not in EXTENSOES_PERMITIDAS:

            await update.message.reply_text(
                text=(
                    "❌ Este tipo de arquivo não é permitido.\n\n"
                    "Formatos aceitos:\n"
                    "• PDF\n"
                    #"• DOCX\n"
                    #"• TXT\n"
                    "• JPG\n"
                    "• JPEG\n"
                    "• PNG\n"
                    #"• WEBP\n"
                    #"• HEIC"
                ),
            )

            return

        # ------------------------
        # Validação do tamanho
        # ------------------------
        if (
            arquivo.file_size
            and arquivo.file_size > MAX_TAMANHO_BYTES
        ):

            await update.message.reply_text(
                text=(
                    f"❌ O arquivo excede o tamanho máximo permitido de "
                    f"{MAX_TAMANHO_MB} MB."
                ),
            )

            return

        # ------------------------
        # Descobre o TIPO do arquivo
        # ------------------------
        if extensao == ".pdf":

            tipo = "pdf"
            prefixo = "pdf"

        elif extensao == ".docx":

            tipo = "docx"
            prefixo = "documento"

        elif extensao == ".txt":

            tipo = "txt"
            prefixo = "texto"

        elif extensao in {
            ".jpg",
            ".jpeg",
            ".png",
            ".heic",
            ".webp",
        }:

            tipo = "imagem"
            prefixo = "pagina"

        telegram_file = await arquivo.get_file()

        file_id = arquivo.file_id

    elif update.message.photo:

        foto = update.message.photo[-1]

        if (
            foto.file_size
            and foto.file_size > MAX_TAMANHO_BYTES
        ):

            await update.message.reply_text(
                text=(
                    f"❌ O arquivo excede o tamanho máximo permitido de "
                    f"{MAX_TAMANHO_MB} MB."
                ),
            )

            return

        tipo = "imagem"
        prefixo = "pagina"

        # Fotos enviadas como imagem do Telegram
        # sempre chegam convertidas para JPG.
        extensao = ".jpg"

        telegram_file = await foto.get_file()

        file_id = foto.file_id

    # ------------------------
    # Só continua se um arquivo
    # realmente foi identificado.
    # ------------------------
    if telegram_file is None:

        return

    quantidade_do_tipo = sum(
        1
        for arquivo_salvo
        in context.user_data["arquivos"]
        if arquivo_salvo["tipo"] == tipo
    )

    nome_arquivo = (
        f"{prefixo}_{quantidade_do_tipo + 1}{extensao}"
    )

    caminho = pasta_envio / nome_arquivo

    try:

        await telegram_file.download_to_drive(
            caminho
        )

    except Exception as erro:

        logger.error(
            f"Erro ao salvar arquivo enviado: {erro}",
            exc_info=True,
        )

        await update.message.reply_text(
            "❌ Não foi possível salvar o arquivo. Tente novamente."
        )

        return

    # ------------------------
    # Validação da assinatura
    # ------------------------
    if not validar_assinatura(caminho):

        caminho.unlink(
            missing_ok=True
        )

        await update.message.reply_text(
            text=(
                "❌ O conteúdo do arquivo não corresponde à extensão enviada.\n\n"
                "Verifique o arquivo e tente novamente."
            ),
        )

        return

    context.user_data["arquivos"].append(
        {
            "tipo": tipo,
            "file_id": file_id,
            "nome": nome_arquivo,
            "caminho": caminho,
        }
    )

    quantidade = len(
        context.user_data["arquivos"]
    )

    # ------------------------
    # Remove a mensagem anterior
    # de acompanhamento do upload.
    #
    # IMPORTANTE:
    # também remove o ID da lista
    # do /clean, pois a mensagem já
    # foi apagada aqui.
    # ------------------------
    message_id = context.user_data.get(
        "mensagem_upload_id"
    )

    if message_id:

        try:

            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=message_id,
            )

        except Exception as erro:

            logger.warning(
                f"Não foi possível apagar a "
                f"mensagem: {erro}"
            )

        # Remove o ID que já foi tratado
        # da lista usada pelo /clean.
        clean_messages = context.user_data.get(
            "clean_messages",
            [],
        )

        context.user_data["clean_messages"] = [
            mensagem_id
            for mensagem_id in clean_messages
            if mensagem_id != message_id
        ]

    # ------------------------
    # Cria a nova mensagem
    # de acompanhamento.
    # ------------------------
    mensagem = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MENSAGEM_UPLOAD.format(
            total=quantidade,
        ),
        reply_markup=teclado_finalizar(),
    )

    context.user_data["mensagem_upload_id"] = (
        mensagem.message_id
    )

    # Registra a nova mensagem
    # para o /clean.
    add_clean_message(
        context,
        mensagem.message_id,
    )