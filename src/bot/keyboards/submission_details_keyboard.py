from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


def submission_details_keyboard(
    review_index: int,
    submission_index: int,
):

    teclado = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📂 Ver arquivos",
                    callback_data=(
                        f"submission:files:"
                        f"{review_index}:"
                        f"{submission_index}"
                    ),
                )
            ],
        ]
    )

    return teclado