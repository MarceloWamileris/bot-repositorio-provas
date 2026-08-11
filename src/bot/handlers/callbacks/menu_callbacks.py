from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import ContextTypes

from bot.keyboards.menu_keyboard import (
    menu_keyboard,
)

from messages.menu import (
    MENSAGEM_MENU_PRINCIPAL,
)

from messages.envio import (
    MENSAGEM_INSTRUCOES,
)

from bot.keyboards.upload_keyboard import (
    teclado_instrucoes,
)

from bot.utils.clean_messages import (
    add_clean_message,
)


async def callback_enviar(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    # DEBUG
    print(
        "[DEBUG ENVIAR] ID:",
        query.message.message_id,
    )

    # Limpa qualquer envio anterior
    context.user_data["arquivos"] = []

    context.user_data.pop(
        "contador_msg_id",
        None,
    )

    # Registra a mensagem que será utilizada
    # como tela de instruções/upload
    add_clean_message(
        context,
        query.message.message_id,
    )

    await query.edit_message_text(
        text=MENSAGEM_INSTRUCOES,
        reply_markup=teclado_instrucoes(),
    )


async def callback_voltar_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        text=MENSAGEM_MENU_PRINCIPAL,
        reply_markup=menu_keyboard(),
    )


async def callback_consultar(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        text="📚 Onde você deseja consultar?",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📁 GitHub",
                        callback_data="consultar:github",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📚 Telegram",
                        callback_data="consultar:telegram",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⬅️ Voltar ao menu",
                        callback_data="voltar_menu",
                    )
                ],
            ]
        ),
    )


async def callback_consultar_github(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        text="📁 Repositório do GitHub",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔗 Acessar GitHub",
                        url=(
                            "https://github.com/"
                            "MarceloWamileris/"
                            "repositorio-provas-faeterj"
                        ),
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⬅️ Voltar",
                        callback_data="consultar",
                    )
                ],
            ]
        ),
    )


async def callback_consultar_telegram(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        text="📚 Repositório do Telegram",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔗 Acessar Telegram",
                        url=(
                            "https://t.me/"
                            "+fj-6zGcNEkw5NTZh"
                        ),
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⬅️ Voltar",
                        callback_data="consultar",
                    )
                ],
            ]
        ),
    )


async def callback_ajuda(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        "❓ Você escolheu ajuda.",
    )