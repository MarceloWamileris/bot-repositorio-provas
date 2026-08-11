from telegram import Update
from telegram.ext import ContextTypes

from bot.utils.clean_messages import (
    clear_clean_messages,
)


async def clean(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await clear_clean_messages(
        context=context,
        chat_id=update.effective_chat.id,
    )