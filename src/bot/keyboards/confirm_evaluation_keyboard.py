from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def confirm_evaluation_keyboard(
    is_avs: bool,
):
    """
    Teclado da tela de confirmação.

    is_avs = True
        Volta para Avaliação Vinculada.

    is_avs = False
        Volta para Avaliação.
    """

    callback_back = (
        "back:confirm_linked_evaluation"
        if is_avs
        else "back:confirm_evaluation"
    )

    teclado = [
        [
            InlineKeyboardButton(
                text="✅ Confirmar",
                callback_data="confirm:evaluation",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Voltar",
                callback_data=callback_back,
            ),
        ],
    ]

    return InlineKeyboardMarkup(
        teclado,
    )