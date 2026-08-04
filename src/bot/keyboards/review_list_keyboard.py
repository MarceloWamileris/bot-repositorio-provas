from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


def review_list_keyboard(
    revisoes: list,
):

    teclado = []

    for revisao in revisoes:

        avaliacao = revisao["avaliacao"]

        quantidade = revisao["quantidade"]

        texto = (
            f"{avaliacao['codigo_disciplina']} • "
            f"{avaliacao['avaliacao']}"
        )

        if quantidade > 1:

            texto += f" ({quantidade})"

        teclado.append(
            [
                InlineKeyboardButton(
                    text=texto,
                    callback_data=f"review:{revisao['indice']}",
                )
            ]
        )

    return InlineKeyboardMarkup(
        teclado
    )
    