from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards.menu_keyboard import menu_keyboard
from messages.menu import MENSAGEM_MENU_PRINCIPAL


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        MENSAGEM_MENU_PRINCIPAL,
        reply_markup=menu_keyboard(),
    )