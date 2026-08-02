from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def criar_teclado_finalizar():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ Finalizar envio",
                    callback_data="finalizar_upload",
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Voltar",
                    callback_data="enviar",
                )
            ],
        ]
    )