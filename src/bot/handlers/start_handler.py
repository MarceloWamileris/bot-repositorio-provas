from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    teclado = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📄 Enviar avaliação",
                    callback_data="enviar",
                )
            ],
            [
                InlineKeyboardButton(
                    "📚 Consultar Acervo",
                    callback_data="consultar",
                )
            ],
            [
                InlineKeyboardButton(
                    "❓ Ajuda",
                    callback_data="ajuda",
                )
            ],
        ]
    )

    await update.message.reply_text(
        "📚 Repositório de Provas (FAETERJ ADS)\n\n"
        "Escolha uma opção:",
        reply_markup=teclado,
    )