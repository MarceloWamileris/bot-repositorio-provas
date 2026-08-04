from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


def submission_details_keyboard(
    review_index: int,
):

    teclado = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📂 Ver arquivos",
                    callback_data=(
                        f"submission:files:{review_index}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Voltar",
                    callback_data=(
                        f"review:{review_index}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "✅ Aprovar esta versão",
                    callback_data=(
                        f"submission:approve:{review_index}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "❌ Rejeitar esta versão",
                    callback_data=(
                        f"submission:reject:{review_index}"
                    ),
                )
            ],
        ]
    )

    return teclado