from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


def menu_keyboard():

    teclado = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📄 Enviar avaliação",
                    callback_data="enviar",
                )
            ],
            [
                InlineKeyboardButton(
                    "📚 Consultar Acervo",
                    callback_data="consultar",
                )
            ],
            [
                InlineKeyboardButton(
                    "❓ Ajuda",
                    callback_data="ajuda",
                )
            ],
        ]
    )

    return teclado