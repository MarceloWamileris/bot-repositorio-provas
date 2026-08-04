from telegram import Update
from telegram.ext import ContextTypes

from services.review_queue_service import (
    ReviewQueueService,
)
from bot.keyboards.submission_details_keyboard import (
    submission_details_keyboard,
)
from bot.keyboards.submission_action_keyboard import (
    submission_action_keyboard,
)
from bot.keyboards.submission_success_keyboard import (
    submission_success_keyboard,
)
from bot.handlers.callbacks.review_admin_callbacks import (
    enviar_detalhes_revisao,
)

async def callback_submission_details(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    _, review_index, submission_index = (
        query.data.split(":")
    )
    review_index = int(review_index)
    submission_index = int(submission_index)

    revisoes = ReviewQueueService.listar()
    grupo = next(
        (
            revisao
            for revisao in revisoes
            if revisao["indice"] == review_index
        ),
        None,
    )

    if grupo is None:
        await query.edit_message_text(
            "⚠️ Esta revisão não está mais disponível."
        )
        return

    submissao = grupo["submissoes"][submission_index]

    await query.edit_message_text(
        text=(
            f"📄 Versão {submission_index + 1}\n\n"
            f"Usuário: {submissao['usuario_id']}\n"
            f"Arquivos enviados: {len(submissao['arquivos'])}"
        ),
        reply_markup=submission_details_keyboard(
            review_index,
            submission_index,
        ),
    )


async def callback_submission_files(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    # Apaga a tela da versão
    await query.message.delete()

    # Inicia a lista de mensagens desta revisão
    context.user_data["review_messages"] = []

    _, _, review_index, submission_index = (
        query.data.split(":")
    )
    review_index = int(review_index)
    submission_index = int(submission_index)

    revisoes = ReviewQueueService.listar()

    grupo = next(
        (
            revisao
            for revisao in revisoes
            if revisao["indice"] == review_index
        ),
        None,
    )

    if grupo is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Esta revisão não está mais disponível.",
        )
        return

    submissao = grupo["submissoes"][submission_index]
    avaliacao = grupo["avaliacao"]

    # Cabeçalho
    msg = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📂 VERSÃO {submission_index + 1} DE {grupo['quantidade']}\n\n"
            f"Disciplina: {avaliacao['codigo_disciplina']}\n"
            f"Professor: {avaliacao['nome_professor']}\n"
            f"Ano/Semestre: "
            f"{avaliacao['ano']}-"
            f"{avaliacao['semestre']}\n"
            f"Turno: {avaliacao['turno']}\n"
            f"Avaliação: {avaliacao['avaliacao']}\n\n"
            f"Arquivos enviados: "
            f"{len(submissao['arquivos'])}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Os arquivos desta versão estão logo abaixo."
        ),
    )

    context.user_data["review_messages"].append(
        msg.message_id
    )

    # Arquivos
    for arquivo in submissao["arquivos"]:

        if arquivo["tipo"] == "imagem":

            msg = await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=arquivo["file_id"],
            )

            context.user_data["review_messages"].append(
                msg.message_id
            )

        elif arquivo["tipo"] == "pdf":

            msg = await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=arquivo["file_id"],
            )

            context.user_data["review_messages"].append(
                msg.message_id
            )

    possui_outras_versoes = (
        grupo["quantidade"] > 1
    )

    # Botões
    msg = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="📄 O que deseja fazer com esta versão?",
        reply_markup=submission_action_keyboard(
            review_index,
            submission_index,
            possui_outras_versoes,
        ),
    )

    context.user_data["review_messages"].append(
        msg.message_id
    )

    print(context.user_data["review_messages"])


async def callback_submission_approve(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    # Apaga todas as mensagens da revisão
    for message_id in context.user_data.get(
        "review_messages",
        []
    ):
        try:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=message_id,
            )
        except Exception:
            pass

    context.user_data["review_messages"] = []

    _, _, review_index, submission_index = (
        query.data.split(":")
    )

    review_index = int(review_index)
    submission_index = int(submission_index)

    grupos = ReviewQueueService.listar()

    grupo = next(
        (
            revisao
            for revisao in grupos
            if revisao["indice"] == review_index
        ),
        None,
    )

    if grupo is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Esta revisão não está mais disponível.",
        )
        return

    havia_multiplas_versoes = (
        grupo["quantidade"] > 1
    )

    if havia_multiplas_versoes:
        sucesso = ReviewQueueService.remover_revisao(
            review_index,
        )
    else:
        sucesso = ReviewQueueService.remover_submissao(
            review_index,
            submission_index,
        )

    if not sucesso:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Esta revisão não está mais disponível.",
        )
        return

    if havia_multiplas_versoes:
        mensagem = (
            "✅ Versão aprovada com sucesso!\n\n"
            "As demais versões desta prova foram descartadas "
            "e a revisão foi concluída."
        )
    else:
        mensagem = (
            "✅ Versão aprovada com sucesso!\n\n"
            "A revisão desta prova foi concluída."
        )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=mensagem,
        reply_markup=submission_success_keyboard(),
    )


async def callback_submission_reject(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    # Apaga todas as mensagens da revisão
    for message_id in context.user_data.get(
        "review_messages",
        []
    ):
        try:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=message_id,
            )
        except Exception:
            pass

    context.user_data["review_messages"] = []

    _, _, review_index, submission_index = (
        query.data.split(":")
    )

    review_index = int(review_index)
    submission_index = int(submission_index)

    revisoes = ReviewQueueService.listar()

    grupo = next(
        (
            revisao
            for revisao in revisoes
            if revisao["indice"] == review_index
        ),
        None,
    )

    if grupo is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Esta revisão não está mais disponível.",
        )
        return

    chave = (
        grupo["avaliacao"]["codigo_disciplina"],
        grupo["avaliacao"]["id_professor"],
        grupo["avaliacao"]["ano"],
        grupo["avaliacao"]["semestre"],
        grupo["avaliacao"]["turno"],
        grupo["avaliacao"]["avaliacao"],
    )

    sucesso = ReviewQueueService.remover_submissao(
        review_index,
        submission_index,
    )

    if not sucesso:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Esta revisão não está mais disponível.",
        )
        return

    revisoes = ReviewQueueService.listar()

    grupo = next(
        (
            revisao
            for revisao in revisoes
            if (
                revisao["avaliacao"]["codigo_disciplina"],
                revisao["avaliacao"]["id_professor"],
                revisao["avaliacao"]["ano"],
                revisao["avaliacao"]["semestre"],
                revisao["avaliacao"]["turno"],
                revisao["avaliacao"]["avaliacao"],
            ) == chave
        ),
        None,
    )

    if grupo is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                "❌ Versão rejeitada.\n\n"
                "Não existem mais versões desta prova."
            ),
            reply_markup=submission_success_keyboard(),
        )
        return

    await enviar_detalhes_revisao(
        chat_id=update.effective_chat.id,
        context=context,
        grupo=grupo,
        mensagem=(
            "❌ Versão rejeitada.\n\n"
            "Ainda existem outras versões para análise."
        ),
    )