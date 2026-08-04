from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


def review_details_keyboard(
    grupo: dict,
):

    teclado = []

    for indice, _ in enumerate(
        grupo["submissoes"],
    ):

        teclado.append(
            [
                InlineKeyboardButton(
                    text=f"📄 Versão {indice + 1}",
                    callback_data=(
                        f"submission:{grupo['indice']}:{indice}"
                    ),
                )
            ]
        )

    return InlineKeyboardMarkup(
        teclado
    )