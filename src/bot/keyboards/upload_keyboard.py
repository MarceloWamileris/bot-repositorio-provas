from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def teclado_instrucoes():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ Entendi",
                    callback_data="upload",
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Voltar",
                    callback_data="voltar_menu",
                )
            ],
        ]
    )