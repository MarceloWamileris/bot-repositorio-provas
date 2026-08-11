from telegram.ext import ContextTypes


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

        print(
            f"[CLEAN] Mensagem registrada: {message_id}"
        )


async def clear_clean_messages(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
):

    message_ids = context.user_data.get(
        "clean_messages",
        [],
    )

    print(
        "[CLEAN] IDs registrados:",
        message_ids,
    )

    for message_id in message_ids:

        try:

            print(
                f"[CLEAN] Tentando apagar: {message_id}"
            )

            await context.bot.delete_message(
                chat_id=chat_id,
                message_id=message_id,
            )

            print(
                f"[CLEAN] Apagou: {message_id}"
            )

        except Exception as erro:

            print(
                f"[CLEAN] Mensagem {message_id} "
                f"já não existe ou não pôde ser apagada: {erro}"
            )

    # Depois do /clean, começa uma nova lista
    context.user_data["clean_messages"] = []