from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from data.catalogo_professores import (
    CATALOGO_PROFESSORES,
)


def teclado_professores():

    teclado = []

    linha = []

    for professor in CATALOGO_PROFESSORES:

        linha.append(
            InlineKeyboardButton(
                text=professor["exibicao"],
                callback_data=f"professor:{professor['id']}",
            )
        )

        if len(linha) == 2:

            teclado.append(linha)
            linha = []

    if linha:

        teclado.append(linha)

    return InlineKeyboardMarkup(teclado)