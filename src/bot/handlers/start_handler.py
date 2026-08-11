from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards.menu_keyboard import (
    menu_keyboard,
)

from messages.menu import (
    MENSAGEM_MENU_PRINCIPAL,
)

from bot.utils.clean_messages import (
    add_clean_message,
)


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    # --------------------------------------------------
    # Remove o menu principal anterior, se existir
    # --------------------------------------------------
    menu_anterior_id = context.user_data.get(
        "menu_principal_id"
    )

    if menu_anterior_id:

        try:

            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=menu_anterior_id,
            )

        except Exception as erro:

            print(
                f"ERRO AO APAGAR MENU ANTERIOR: {erro}"
            )

    # --------------------------------------------------
    # Cria o novo menu principal
    # --------------------------------------------------
    mensagem = await update.message.reply_text(
        MENSAGEM_MENU_PRINCIPAL,
        reply_markup=menu_keyboard(),
    )

    # Guarda o ID do novo menu
    context.user_data[
        "menu_principal_id"
    ] = mensagem.message_id

    # Registra a mensagem para o /clean
    add_clean_message(
        context,
        mensagem.message_id,
    )