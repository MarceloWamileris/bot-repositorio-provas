from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def linked_evaluation_keyboard():

    teclado = [
        [
            InlineKeyboardButton(
                text="📝 AV1",
                callback_data="vinculada:AV1",
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 AV2",
                callback_data="vinculada:AV2",
            )
        ],
    ]

    return InlineKeyboardMarkup(teclado)