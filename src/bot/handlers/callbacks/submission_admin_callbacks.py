import traceback

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
from bot.utils.review_messages import (
    add_review_message,
    clear_review_messages,
)
from services.storage_service import (
    StorageService,
)

from services.file_service import (
    FileService,
)

from services.file_service import (
    FileService,
)

MSG_REVISAO_INDISPONIVEL = (
    "⚠️ Esta revisão não está mais disponível."
)
MSG_VERSAO_INDISPONIVEL = (
    "⚠️ Esta versão não existe mais."
)


# ------------------------------------------------------
# Helpers
# ------------------------------------------------------

def buscar_grupo(review_index: int):
    """
    Busca um grupo de revisão pelo índice.
    Retorna None se ele não existir mais (ex: já foi
    aprovado/rejeitado por outro admin).
    """
    revisoes = ReviewQueueService.listar()

    return next(
        (
            revisao
            for revisao in revisoes
            if revisao["indice"] == review_index
        ),
        None,
    )


def buscar_grupo_por_chave(chave):
    """
    Busca um grupo de revisão pela chave da avaliação
    (usado após remover uma submissão, quando o índice
    original pode ter mudado).
    """
    revisoes = ReviewQueueService.listar()

    return next(
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
            )
            == chave
        ),
        None,
    )


def chave_da_avaliacao(grupo):
    return (
        grupo["avaliacao"]["codigo_disciplina"],
        grupo["avaliacao"]["id_professor"],
        grupo["avaliacao"]["ano"],
        grupo["avaliacao"]["semestre"],
        grupo["avaliacao"]["turno"],
        grupo["avaliacao"]["avaliacao"],
    )


def buscar_submissao(grupo, submission_index: int):
    """
    Retorna a submissão pelo índice, ou None se o índice
    estiver fora do intervalo válido. Protege contra
    IndexError vindo de callbacks antigos/desatualizados.
    """
    if grupo is None:
        return None

    submissoes = grupo["submissoes"]

    if submission_index < 0:
        return None

    if submission_index >= len(submissoes):
        return None

    return grupo["submissoes"][submission_index]


# ------------------------------------------------------
# Handlers
# ------------------------------------------------------

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

    grupo = buscar_grupo(review_index)

    if grupo is None:
        await query.edit_message_text(MSG_REVISAO_INDISPONIVEL)
        return

    submissao = buscar_submissao(grupo, submission_index)

    if submissao is None:
        await query.edit_message_text(MSG_VERSAO_INDISPONIVEL)
        return

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


async def mostrar_submissao(
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE,
    review_index: int,
    submission_index: int,
):
    grupo = buscar_grupo(review_index)

    if grupo is None:
        await context.bot.send_message(
            chat_id=chat_id,
            text=MSG_REVISAO_INDISPONIVEL,
        )
        return

    submissao = buscar_submissao(grupo, submission_index)

    if submissao is None:
        await context.bot.send_message(
            chat_id=chat_id,
            text=MSG_VERSAO_INDISPONIVEL,
        )
        return

    avaliacao = grupo["avaliacao"]
    total_versoes = len(grupo["submissoes"])

    # ------------------------
    # Cabeçalho
    # ------------------------
    msg = await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📂 VERSÃO {submission_index + 1} DE {total_versoes}\n\n"
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
    add_review_message(context, msg.message_id)

    # ------------------------
    # Arquivos
    # ------------------------
    for arquivo in submissao["arquivos"]:
        if arquivo["tipo"] == "imagem":
            msg = await context.bot.send_photo(
                chat_id=chat_id,
                photo=arquivo["file_id"],
            )
            add_review_message(context, msg.message_id)
        elif arquivo["tipo"] == "pdf":
            msg = await context.bot.send_document(
                chat_id=chat_id,
                document=arquivo["file_id"],
            )
            add_review_message(context, msg.message_id)

    # ------------------------
    # Debug
    # ------------------------
    print("=" * 40)
    print("DEBUG")
    print(f"review_index     = {review_index}")
    print(f"submission_index = {submission_index}")
    print(f"total_versoes    = {total_versoes}")
    print(f"len(submissoes)  = {len(grupo['submissoes'])}")
    print("=" * 40)

    # ------------------------
    # Botões
    # ------------------------
    msg = await context.bot.send_message(
        chat_id=chat_id,
        text="📄 O que deseja fazer com esta versão?",
        reply_markup=submission_action_keyboard(
            review_index,
            submission_index,
            total_versoes,
        ),
    )
    add_review_message(context, msg.message_id)


async def callback_submission_files(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    # remove o menu da versão
    try:
        await query.message.delete()
    except Exception:
        pass

    # limpa mensagens da versão anterior
    await clear_review_messages(
        context=context,
        chat_id=update.effective_chat.id,
    )

    _, _, review_index, submission_index = (
        query.data.split(":")
    )

    review_index = int(review_index)
    submission_index = int(submission_index)

    grupo = buscar_grupo(review_index)

    if grupo is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=MSG_REVISAO_INDISPONIVEL,
        )
        return

    submissao = buscar_submissao(
        grupo,
        submission_index,
    )

    print("=" * 50)
    print("GRUPO:")
    print(grupo)
    print("=" * 50)

    if submissao is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=MSG_VERSAO_INDISPONIVEL,
        )
        return

    # DEBUG: Verificando estrutura do grupo
    print("CHAVES DO GRUPO:")
    print(grupo.keys())
    print("TIPO:", grupo.get("tipo"))
    print("=" * 80)
    print("GRUPO COMPLETO:")
    print(grupo)
    print("=" * 80)

    if grupo["tipo"] == "comparacao":
        from bot.handlers.callbacks.submission_compare_callbacks import (
            mostrar_comparacao,
        )

        await mostrar_comparacao(
            chat_id=update.effective_chat.id,
            context=context,
            grupo=grupo,
            submission_index=submission_index,
        )
    else:
        await mostrar_submissao(
            chat_id=update.effective_chat.id,
            context=context,
            review_index=review_index,
            submission_index=submission_index,
        )


async def callback_submission_next(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    # Nota: query.answer() precisa ficar após a checagem de
    # erro, pois o Telegram só aceita uma resposta por
    # callback_query. Não é possível responder antecipadamente
    # e depois usar show_alert=True no caminho de erro.

    _, _, review_index, submission_index = (
        query.data.split(":")
    )
    review_index = int(review_index)
    submission_index = int(submission_index)

    grupo = buscar_grupo(review_index)

    if grupo is None:
        await query.answer(
            MSG_REVISAO_INDISPONIVEL,
            show_alert=True,
        )
        return

    novo_indice = submission_index + 1

    if novo_indice >= len(grupo["submissoes"]):
        await query.answer(
            "Esta já é a última versão.",
            show_alert=True,
        )
        return

    await query.answer()

    await clear_review_messages(
        context=context,
        chat_id=update.effective_chat.id,
    )

    await mostrar_submissao(
        chat_id=update.effective_chat.id,
        context=context,
        review_index=review_index,
        submission_index=novo_indice,
    )


async def callback_submission_previous(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    # Mesma observação de callback_submission_next: o answer()
    # tem que ficar depois da checagem de erro.

    _, _, review_index, submission_index = (
        query.data.split(":")
    )
    review_index = int(review_index)
    submission_index = int(submission_index)

    grupo = buscar_grupo(review_index)

    if grupo is None:
        await query.answer(
            MSG_REVISAO_INDISPONIVEL,
            show_alert=True,
        )
        return

    novo_indice = submission_index - 1

    if novo_indice < 0:
        await query.answer(
            "Esta já é a primeira versão.",
            show_alert=True,
        )
        return

    await query.answer()

    await clear_review_messages(
        context=context,
        chat_id=update.effective_chat.id,
    )

    await mostrar_submissao(
        chat_id=update.effective_chat.id,
        context=context,
        review_index=review_index,
        submission_index=novo_indice,
    )


async def callback_submission_approve(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    _, _, review_index, submission_index = (
        query.data.split(":")
    )
    review_index = int(review_index)
    submission_index = int(submission_index)

    grupo = buscar_grupo(review_index)

    if grupo is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=MSG_REVISAO_INDISPONIVEL,
        )
        return

    submissao = buscar_submissao(
        grupo,
        submission_index,
    )

    if submissao is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=MSG_VERSAO_INDISPONIVEL,
        )
        return

    try:
        for arquivo in submissao["arquivos"]:
            StorageService.armazenar_arquivo(
                grupo["avaliacao"],
                arquivo["caminho"],
            )

        if submissao["arquivos"]:

            pasta_envio = (
            submissao["arquivos"][0]["caminho"].parent
        )

        FileService.remover_pasta_envio(
            pasta_envio,
        )

    except Exception as erro:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                "❌ Ocorreu um erro ao salvar os arquivos.\n"
                "A revisão não foi removida da fila."
            ),
        )
        traceback.print_exc()
        return

    await clear_review_messages(
        context=context,
        chat_id=update.effective_chat.id,
    )

    havia_multiplas_versoes = len(grupo["submissoes"]) > 1

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
            text=MSG_REVISAO_INDISPONIVEL,
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

    _, _, review_index, submission_index = (
        query.data.split(":")
    )
    review_index = int(review_index)
    submission_index = int(submission_index)

    grupo = buscar_grupo(review_index)

    if grupo is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=MSG_REVISAO_INDISPONIVEL,
        )
        return

    chave = chave_da_avaliacao(grupo)

    # Remove todas as mensagens da versão atual
    await clear_review_messages(
        context=context,
        chat_id=update.effective_chat.id,
    )

    sucesso = ReviewQueueService.remover_submissao(
        review_index,
        submission_index,
    )

    if not sucesso:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=MSG_REVISAO_INDISPONIVEL,
        )
        return

    # Recarrega a fila pela chave (o índice pode ter mudado)
    grupo = buscar_grupo_por_chave(chave)

    # Não existe mais nenhuma versão
    if grupo is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ Todas as versões desta prova foram rejeitadas.",
            reply_markup=submission_success_keyboard(),
        )
        return

    # Ainda existem versões -> mostra a versão mais próxima
    # da posição em que o administrador estava
    novo_indice = min(
        submission_index,
        len(grupo["submissoes"]) - 1,
    )

    await mostrar_submissao(
        chat_id=update.effective_chat.id,
        context=context,
        review_index=grupo["indice"],
        submission_index=novo_indice,
    )