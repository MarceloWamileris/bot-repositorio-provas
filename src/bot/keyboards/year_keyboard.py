from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def teclado_ano():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="⬅️ Voltar",
                    callback_data="voltar:professor",
                )
            ]
        ]
    )