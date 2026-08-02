from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def teclado_finalizar():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ Finalizar envio",
                    callback_data="finalizar_envio",
                )
            ]
        ]
    )