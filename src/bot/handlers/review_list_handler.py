from telegram import Update
from telegram.ext import ContextTypes

from services.review_queue_service import (
    ReviewQueueService,
)

from bot.keyboards.review_list_keyboard import (
    review_list_keyboard,
)


async def enviar_lista_revisoes(
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE,
):

    revisoes = ReviewQueueService.listar()

    if len(revisoes) == 0:

        await context.bot.send_message(
            chat_id=chat_id,
            text="📭 Não há revisões pendentes.",
        )

        return

    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "📋 Revisões pendentes\n\n"
            "⬇️ Selecione uma revisão:"
        ),
        reply_markup=review_list_keyboard(
            revisoes,
        ),
    )


async def listar_revisoes(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    await enviar_lista_revisoes(
        update.effective_chat.id,
        context,
    )