from telegram import Update
from telegram.ext import ContextTypes

from messages.upload import MENSAGEM_UPLOAD

from bot.keyboards.finish_keyboard import (
    teclado_finalizar,
)

from services.file_service import (
    FileService,
)

from services.upload_cleanup_service import (
    UploadCleanupService,
)


async def upload(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    context.user_data["etapa"] = "upload"

    context.user_data["arquivos"] = []

    # Reinicia o controle de álbuns (media groups)
    context.user_data["ultimo_media_group"] = None

    # Limpa uploads temporários expirados
    await UploadCleanupService.limpar_expirados()

    context.user_data["pasta_envio"] = (
        FileService.criar_pasta_envio(
            update.effective_user.id
        )
    )

    # Registra este novo upload no status.json
    UploadCleanupService.registrar_upload(
        usuario_id=update.effective_user.id,
        pasta=context.user_data["pasta_envio"],
    )

    mensagem = await query.edit_message_text(
        text=MENSAGEM_UPLOAD.format(
            total=0,
        ),
        reply_markup=teclado_finalizar(),
    )

    context.user_data["mensagem_upload_id"] = (
        mensagem.message_id
    )

