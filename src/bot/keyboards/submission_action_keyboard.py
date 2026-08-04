from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


def submission_action_keyboard(
    review_index: int,
    submission_index: int,
    quantidade_versoes: int,
):
    print("=" * 40)
    print("KEYBOARD")
    print(f"submission_index = {submission_index}")
    print(f"quantidade_versoes = {quantidade_versoes}")
    print(f"condicao proxima = {submission_index < quantidade_versoes - 1}")
    print("=" * 40)

    teclado = []

    # -------------------------
    # Navegação entre versões
    # -------------------------

    navegacao = []

    if submission_index > 0:
        navegacao.append(
            InlineKeyboardButton(
                text="⬅️ Anterior",
                callback_data=(
                    f"submission:previous:"
                    f"{review_index}:"
                    f"{submission_index}"
                ),
            )
        )

    if submission_index < quantidade_versoes - 1:
        navegacao.append(
            InlineKeyboardButton(
                text="➡️ Próxima",
                callback_data=(
                    f"submission:next:"
                    f"{review_index}:"
                    f"{submission_index}"
                ),
            )
        )

    if navegacao:
        teclado.append(navegacao)

    # -------------------------
    # Aprovar
    # -------------------------

    teclado.append(
        [
            InlineKeyboardButton(
                text="✅ Aprovar esta versão",
                callback_data=(
                    f"submission:approve:"
                    f"{review_index}:"
                    f"{submission_index}"
                ),
            )
        ]
    )

    # -------------------------
    # Rejeitar
    # -------------------------

    teclado.append(
        [
            InlineKeyboardButton(
                text="❌ Rejeitar esta versão",
                callback_data=(
                    f"submission:reject:"
                    f"{review_index}:"
                    f"{submission_index}"
                ),
            )
        ]
    )

    # -------------------------
    # Voltar
    # -------------------------

    teclado.append(
        [
            InlineKeyboardButton(
                text="📋 Voltar para revisões",
                callback_data="review:list",
            )
        ]
    )

    return InlineKeyboardMarkup(teclado)