from telegram import Update
from telegram.ext import ContextTypes

from services.review_queue_service import (
    ReviewQueueService,
)

from bot.keyboards.review_list_keyboard import (
    review_list_keyboard,
)


async def listar_revisoes(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    revisoes = ReviewQueueService.listar()

    if len(revisoes) == 0:

        await update.message.reply_text(
            "📭 Não há revisões pendentes."
        )

        return

    await update.message.reply_text(
        text=(
            "📋 Revisões pendentes\n\n"
            "⬇️ Selecione uma revisão:"
        ),
        reply_markup=review_list_keyboard(
            revisoes,
        ),
    )