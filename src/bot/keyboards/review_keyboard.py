from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def review_keyboard():

    teclado = [
        [
            InlineKeyboardButton(
                text="📝 Minha versão deve ser avaliada",
                callback_data="review:request",
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Cancelar envio",
                callback_data="review:cancel",
            )
        ],
    ]

    return InlineKeyboardMarkup(
        teclado,
    )