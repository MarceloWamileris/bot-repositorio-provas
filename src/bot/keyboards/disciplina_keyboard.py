from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from data.catalogo_disciplinas import (
    CATALOGO_DISCIPLINAS,
)


def teclado_disciplinas(
    periodo: str,
):

    teclado = []

    disciplinas = CATALOGO_DISCIPLINAS.get(
        periodo,
        [],
    )

    for disciplina in disciplinas:

        teclado.append(
            [
                InlineKeyboardButton(
                    text=disciplina["codigo"],
                    callback_data=(
                        f"disciplina:{disciplina['codigo']}"
                    ),
                )
            ]
        )

    teclado.append(
        [
            InlineKeyboardButton(
                text="⬅️ Voltar",
                callback_data="voltar:periodo",
            )
        ]
    )

    return InlineKeyboardMarkup(
        teclado,
    )