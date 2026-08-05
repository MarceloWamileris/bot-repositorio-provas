from telegram.ext import ContextTypes


# ------------------------------------------------------
# Mensagens da revisão (versão enviada pelo aluno)
# ------------------------------------------------------

def add_review_message(
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
):
    context.user_data.setdefault(
        "review_messages",
        []
    ).append(message_id)


async def clear_review_messages(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
):
    for message_id in context.user_data.get(
        "review_messages",
        []
    ):
        try:
            await context.bot.delete_message(
                chat_id=chat_id,
                message_id=message_id,
            )
        except Exception:
            pass

    context.user_data["review_messages"] = []


# ------------------------------------------------------
# Mensagens da prova que já existe no acervo
# ------------------------------------------------------

def add_review_acervo_message(
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
):
    context.user_data.setdefault(
        "review_acervo_messages",
        []
    ).append(message_id)


async def clear_review_acervo_messages(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
):
    for message_id in context.user_data.get(
        "review_acervo_messages",
        []
    ):
        try:
            await context.bot.delete_message(
                chat_id=chat_id,
                message_id=message_id,
            )
        except Exception:
            pass

    context.user_data["review_acervo_messages"] = []