from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


def submission_action_keyboard(
    review_index: int,
    submission_index: int,
    possui_outras_versoes: bool,
):

    teclado = [
        [
            InlineKeyboardButton(
                text="✅ Aprovar esta versão",
                callback_data=(
                    f"submission:approve:"
                    f"{review_index}:"
                    f"{submission_index}"
                ),
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Rejeitar esta versão",
                callback_data=(
                    f"submission:reject:"
                    f"{review_index}:"
                    f"{submission_index}"
                ),
            )
        ],
    ]

    if possui_outras_versoes:
        teclado.append(
            [
                InlineKeyboardButton(
                    text="⬅️ Comparar outras versões desta prova",
                    callback_data=f"review:{review_index}",
                )
            ]
        )

    teclado.append(
        [
            InlineKeyboardButton(
                text="📋 Voltar para revisões de outras provas",
                callback_data="review:list",
            )
        ]
    )

    return InlineKeyboardMarkup(teclado)