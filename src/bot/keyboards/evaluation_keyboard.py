from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def evaluation_keyboard():

    teclado = [
        [
            InlineKeyboardButton(
                text="📝 AV1",
                callback_data="avaliacao:AV1",
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 AV2",
                callback_data="avaliacao:AV2",
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 AVS",
                callback_data="avaliacao:AVS",
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 AVF",
                callback_data="avaliacao:AVF",
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Voltar",
                callback_data="voltar:turno",
            )
        ],
    ]

    return InlineKeyboardMarkup(
        teclado,
    )