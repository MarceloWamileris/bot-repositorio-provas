from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


def teclado_turma_fac():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔵 FAC-A",
                    callback_data="fac:FAC-A",
                ),
            ],
            [
                InlineKeyboardButton(
                    "🟠 FAC-B",
                    callback_data="fac:FAC-B",
                ),
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Voltar",
                    callback_data="voltar:fac",
                ),
            ],
        ]
    )