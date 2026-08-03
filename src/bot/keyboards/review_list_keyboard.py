from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


def review_list_keyboard(
    revisoes: list,
):

    teclado = []

    for indice, revisao in enumerate(
        revisoes,
    ):

        avaliacao = revisao["avaliacao"]

        texto = (
            f"{avaliacao['codigo_disciplina']} • "
            f"{avaliacao['nome_professor']} • "
            f"{avaliacao['avaliacao']} • "
            f"{avaliacao['ano']}-{avaliacao['semestre']}"
        )

        teclado.append(
            [
                InlineKeyboardButton(
                    text=texto,
                    callback_data=f"review:{indice}",
                )
            ]
        )

    return InlineKeyboardMarkup(
        teclado
    )