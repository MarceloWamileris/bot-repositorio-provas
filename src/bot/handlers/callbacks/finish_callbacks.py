from telegram import Update
from telegram.ext import ContextTypes

from messages.upload import MENSAGEM_UPLOAD
from bot.keyboards.finish_keyboard import teclado_finalizar
from services.processing_service import ProcessingService


async def callback_finalizar(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    arquivos = context.user_data.get(
        "arquivos",
        [],
    )

    if len(arquivos) == 0:

        await query.edit_message_text(
            text=(
                "⚠️ Você ainda não enviou nenhum arquivo.\n\n"
                "Envie pelo menos um PDF ou uma imagem antes de finalizar o envio.\n\n"
                + MENSAGEM_UPLOAD.format(total=0)
            ),
            reply_markup=teclado_finalizar(),
        )

        return

    await query.edit_message_text(
        "✅ Envio concluído!\n\n"
        f"📄 Arquivos enviados: {len(arquivos)}\n\n"
        "🔄 Aguarde enquanto analisamos sua avaliação.\n"
        "Isso pode levar alguns instantes."
    )

    await ProcessingService.iniciar_processamento(
        update,
        context,
    )