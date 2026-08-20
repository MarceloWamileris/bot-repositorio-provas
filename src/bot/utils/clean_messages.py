import logging

from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


def add_clean_message(
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
):
    mensagens = context.user_data.setdefault(
        "clean_messages",
        [],
    )

    # Evita registrar o mesmo ID duas vezes
    if message_id not in mensagens:

        mensagens.append(message_id)


async def clear_clean_messages(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
):

    message_ids = context.user_data.get(
        "clean_messages",
        [],
    )

    for message_id in message_ids:

        try:

            await context.bot.delete_message(
                chat_id=chat_id,
                message_id=message_id,
            )

        except Exception as erro:

            logger.warning(
                f"Não foi possível apagar a mensagem "
                f"{message_id}: {erro}"
            )

    # Depois do /clean, começa uma nova lista
    context.user_data["clean_messages"] = []