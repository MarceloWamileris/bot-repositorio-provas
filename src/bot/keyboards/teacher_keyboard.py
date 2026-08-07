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

    # Botão de voltar
    teclado.append(
        [
            InlineKeyboardButton(
                text="⬅️ Voltar",
                callback_data="voltar:disciplina",
            )
        ]
    )

    return InlineKeyboardMarkup(teclado)