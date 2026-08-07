from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from data.catalogo_turnos import (
    CATALOGO_TURNOS,
)


def shift_keyboard():

    teclado = []

    emojis = {
        "Manhã": "🌅",
        "Tarde": "🌤️",
        "Noite": "🌙",
    }

    for turno in CATALOGO_TURNOS:

        teclado.append(
            [
                InlineKeyboardButton(
                    text=f"{emojis[turno]} {turno}",
                    callback_data=f"turno:{turno}",
                )
            ]
        )

    # Botão de voltar
    teclado.append(
        [
            InlineKeyboardButton(
                text="⬅️ Voltar",
                callback_data="voltar:semestre",
            )
        ]
    )

    return InlineKeyboardMarkup(
        teclado,
    )