from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


def submission_success_keyboard():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="📋 Voltar para revisões pendentes",
                    callback_data="review:list",
                )
            ]
        ]
    )