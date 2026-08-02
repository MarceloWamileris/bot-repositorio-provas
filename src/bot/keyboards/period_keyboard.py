from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def teclado_periodos():

    teclado = [
        [
            InlineKeyboardButton(
                "1º Período",
                callback_data="periodo:Primeiro Período",
            )
        ],
        [
            InlineKeyboardButton(
                "2º Período",
                callback_data="periodo:Segundo Período",
            )
        ],
        [
            InlineKeyboardButton(
                "3º Período",
                callback_data="periodo:Terceiro Período",
            )
        ],
        [
            InlineKeyboardButton(
                "4º Período",
                callback_data="periodo:Quarto Período",
            )
        ],
        [
            InlineKeyboardButton(
                "5º Período",
                callback_data="periodo:Quinto Período",
            )
        ],
    ]

    return InlineKeyboardMarkup(teclado)