from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


def submission_compare_keyboard(
    review_index: int,
    submission_index: int,
    total_versoes: int,
):

    teclado = []

    navegacao = []

    if submission_index > 0:

        navegacao.append(
            InlineKeyboardButton(
                "⬅️ Anterior",
                callback_data=(
                    f"compare:previous:"
                    f"{review_index}:"
                    f"{submission_index}"
                ),
            )
        )

    if submission_index < total_versoes - 1:

        navegacao.append(
            InlineKeyboardButton(
                "Próxima ➡️",
                callback_data=(
                    f"compare:next:"
                    f"{review_index}:"
                    f"{submission_index}"
                ),
            )
        )

    if navegacao:

        teclado.append(navegacao)

    teclado.append(
        [
            InlineKeyboardButton(
                "✅ Aprovar esta versão",
                callback_data=(
                    f"compare:approve:"
                    f"{review_index}:"
                    f"{submission_index}"
                ),
            )
        ]
    )

    teclado.append(
        [
            InlineKeyboardButton(
                "❌ Rejeitar esta versão",
                callback_data=(
                    f"compare:reject:"
                    f"{review_index}:"
                    f"{submission_index}"
                ),
            )
        ]
    )

    return InlineKeyboardMarkup(teclado)