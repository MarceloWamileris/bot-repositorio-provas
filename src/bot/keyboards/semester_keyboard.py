from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from data.catalogo_semestres import (
    CATALOGO_SEMESTRES,
)


def teclado_semestres(ano: int):

    teclado = []

    for semestre in CATALOGO_SEMESTRES:

        teclado.append(
            [
                InlineKeyboardButton(
                    text=f"{ano}-{semestre}",
                    callback_data=f"semestre:{semestre}",
                )
            ]
        )

    return InlineKeyboardMarkup(teclado)