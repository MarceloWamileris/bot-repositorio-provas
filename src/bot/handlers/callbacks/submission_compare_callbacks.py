from telegram import Update
from telegram.ext import ContextTypes

from services.proof_service import ProofService
from services.review_queue_service import (
    ReviewQueueService,
)

from bot.keyboards.submission_compare_keyboard import (
    submission_compare_keyboard,
)

from bot.utils.review_messages import (
    add_review_acervo_message,
    add_review_message,
    clear_review_messages,
    clear_review_acervo_messages,
)

import traceback

from services.storage_service import StorageService

from services.file_service import (
    FileService,
)

# ------------------------------------------------------
# Helpers
# ------------------------------------------------------

def buscar_grupo(
    review_index: int,
):

    revisoes = ReviewQueueService.listar()

    return next(
        (
            revisao
            for revisao in revisoes
            if revisao["indice"] == review_index
        ),
        None,
    )


def buscar_submissao(
    grupo,
    submission_index: int,
):

    if grupo is None:
        return None

    if submission_index < 0:
        return None

    if submission_index >= len(
        grupo["submissoes"]
    ):
        return None

    return grupo["submissoes"][
        submission_index
    ]


# ------------------------------------------------------
# Exibição da prova do acervo
# ------------------------------------------------------

async def mostrar_acervo(
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE,
    avaliacao: dict,
):
    """
    Exibe a prova atualmente armazenada no acervo.

    Todas as mensagens enviadas por esta função são
    registradas separadamente para que possam ser
    apagadas ao final da revisão.
    """

    paginas = ProofService.obter_paginas(
        avaliacao,
    )

    print("=" * 50)
    print("PAGINAS ENCONTRADAS:")
    print(paginas)
    print("=" * 50)

    if len(paginas) == 0:
        return

    # ------------------------
    # Cabeçalho
    # ------------------------
    msg = await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📚 PROVA ATUAL DO ACERVO\n\n"
            f"Disciplina: {avaliacao['codigo_disciplina']}\n"
            f"Professor: {avaliacao['nome_professor']}\n"
            f"Ano/Semestre: "
            f"{avaliacao['ano']}-"
            f"{avaliacao['semestre']}\n"
            f"Turno: {avaliacao['turno']}\n"
            f"Avaliação: {avaliacao['avaliacao']}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Compare esta prova com a versão enviada pelo aluno."
        ),
    )

    add_review_acervo_message(
        context,
        msg.message_id,
    )

    # ------------------------
    # Arquivos
    # ------------------------
    for pagina in paginas:

        with pagina.open("rb") as arquivo:

            if pagina.suffix.lower() == ".pdf":

                msg = await context.bot.send_document(
                    chat_id=chat_id,
                    document=arquivo,
                )

            else:

                msg = await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=arquivo,
                )

        add_review_acervo_message(
            context,
            msg.message_id,
        )


# ------------------------------------------------------
# Exibição da submissão
# ------------------------------------------------------

async def mostrar_submissao(
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE,
    grupo: dict,
    submission_index: int,
):
    """
    Exibe uma das versões enviadas pelo aluno
    durante a comparação com a prova do acervo.
    """

    submissao = buscar_submissao(
        grupo,
        submission_index,
    )

    if submissao is None:
        return

    avaliacao = grupo["avaliacao"]

    total_versoes = len(
        grupo["submissoes"]
    )

    # ------------------------
    # Cabeçalho
    # ------------------------
    msg = await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📄 VERSÃO {submission_index + 1} "
            f"DE {total_versoes}\n\n"
            f"Disciplina: "
            f"{avaliacao['codigo_disciplina']}\n"
            f"Professor: "
            f"{avaliacao['nome_professor']}\n"
            f"Ano/Semestre: "
            f"{avaliacao['ano']}-"
            f"{avaliacao['semestre']}\n"
            f"Turno: "
            f"{avaliacao['turno']}\n"
            f"Avaliação: "
            f"{avaliacao['avaliacao']}\n\n"
            f"Arquivos enviados: "
            f"{len(submissao['arquivos'])}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Os arquivos desta versão estão logo abaixo."
        ),
    )

    add_review_message(
        context,
        msg.message_id,
    )

    # ------------------------
    # Arquivos
    # ------------------------
    for arquivo in submissao["arquivos"]:

        if arquivo["tipo"] == "imagem":

            msg = await context.bot.send_photo(
                chat_id=chat_id,
                photo=arquivo["file_id"],
            )

        else:

            msg = await context.bot.send_document(
                chat_id=chat_id,
                document=arquivo["file_id"],
            )

        add_review_message(
            context,
            msg.message_id,
        )

    # ------------------------
    # Botões
    # ------------------------
    msg = await context.bot.send_message(
        chat_id=chat_id,
        text="📄 O que deseja fazer com esta versão?",
        reply_markup=submission_compare_keyboard(
            review_index=grupo["indice"],
            submission_index=submission_index,
            total_versoes=total_versoes,
        ),
    )

    add_review_message(
        context,
        msg.message_id,
    )


# ------------------------------------------------------
# Comparação
# ------------------------------------------------------

async def mostrar_comparacao(
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE,
    grupo: dict,
    submission_index: int,
):
    """
    Exibe a comparação entre:

    - prova atualmente armazenada no acervo;
    - versão selecionada da fila de revisão.
    """

    await mostrar_acervo(
        chat_id=chat_id,
        context=context,
        avaliacao=grupo["avaliacao"],
    )

    await mostrar_submissao(
        chat_id=chat_id,
        context=context,
        grupo=grupo,
        submission_index=submission_index,
    )


async def callback_compare_next(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    _, _, review_index, submission_index = (
        query.data.split(":")
    )

    review_index = int(review_index)
    submission_index = int(submission_index)

    grupo = buscar_grupo(
        review_index,
    )

    if grupo is None:

        await query.answer(
            "⚠️ Esta revisão não está mais disponível.",
            show_alert=True,
        )

        return

    novo_indice = submission_index + 1

    if novo_indice >= len(
        grupo["submissoes"]
    ):

        await query.answer(
            "Esta já é a última versão.",
            show_alert=True,
        )

        return

    await query.answer()

    # Remove apenas a versão atual.
    # A prova do acervo permanece.
    await clear_review_messages(
        context=context,
        chat_id=update.effective_chat.id,
    )

    await mostrar_submissao(
        chat_id=update.effective_chat.id,
        context=context,
        grupo=grupo,
        submission_index=novo_indice,
    )


async def callback_compare_previous(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    _, _, review_index, submission_index = (
        query.data.split(":")
    )

    review_index = int(review_index)
    submission_index = int(submission_index)

    grupo = buscar_grupo(
        review_index,
    )

    if grupo is None:

        await query.answer(
            "⚠️ Esta revisão não está mais disponível.",
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

    # Remove apenas a versão atual.
    # A prova do acervo permanece.
    await clear_review_messages(
        context=context,
        chat_id=update.effective_chat.id,
    )

    await mostrar_submissao(
        chat_id=update.effective_chat.id,
        context=context,
        grupo=grupo,
        submission_index=novo_indice,
    )


async def callback_compare_reject(
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

    grupo = buscar_grupo(
        review_index,
    )

    if grupo is None:

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Esta revisão não está mais disponível.",
        )

        return

    submissao = buscar_submissao(
        grupo,
        submission_index,
    )

    if submissao is None:

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Esta versão não existe mais.",
        )

        return

    # Guarda a chave da avaliação
    chave = (
        grupo["avaliacao"]["codigo_disciplina"],
        grupo["avaliacao"]["id_professor"],
        grupo["avaliacao"]["ano"],
        grupo["avaliacao"]["semestre"],
        grupo["avaliacao"]["turno"],
        grupo["avaliacao"]["avaliacao"],
    )

    # Remove apenas as mensagens da submissão atual
    await clear_review_messages(
        context=context,
        chat_id=update.effective_chat.id,
    )

    # Remove a pasta temporária da submissão rejeitada
    # if submissao["arquivos"]:
    #
    #     pasta_envio = (
    #         submissao["arquivos"][0]["caminho"].parent
    #     )
    #
    #     FileService.remover_pasta_envio(
    #         pasta_envio,
    #     )

    if submissao["arquivos"]:

        pasta_envio = (
            submissao["arquivos"][0]["caminho"].parent
    )

        FileService.remover_pasta_envio(
            pasta_envio,
    )

    sucesso = ReviewQueueService.remover_submissao(
        review_index,
        submission_index,
    )

    if not sucesso:

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Não foi possível remover esta versão.",
        )

        return

    # Procura novamente o grupo atualizado
    revisoes = ReviewQueueService.listar()

    grupo = next(
        (
            r
            for r in revisoes
            if (
                r["avaliacao"]["codigo_disciplina"],
                r["avaliacao"]["id_professor"],
                r["avaliacao"]["ano"],
                r["avaliacao"]["semestre"],
                r["avaliacao"]["turno"],
                r["avaliacao"]["avaliacao"],
            ) == chave
        ),
        None,
    )

    # Não restou nenhuma versão
    if grupo is None:

        await clear_review_acervo_messages(
            context=context,
            chat_id=update.effective_chat.id,
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❌ Todas as versões desta prova foram rejeitadas.",
        )

        return

    # Calcula corretamente qual versão mostrar agora
    if submission_index >= len(grupo["submissoes"]):
        novo_indice = len(grupo["submissoes"]) - 1
    else:
        novo_indice = submission_index

    await mostrar_submissao(
        chat_id=update.effective_chat.id,
        context=context,
        grupo=grupo,
        submission_index=novo_indice,
    )


async def callback_compare_approve(
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

    grupo = buscar_grupo(
        review_index,
    )

    if grupo is None:

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Esta revisão não existe mais.",
        )

        return

    submissao = buscar_submissao(
        grupo,
        submission_index,
    )

    if submissao is None:

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Esta versão não existe mais.",
        )

        return

    print("=" * 50)
    print("VERSÕES EXISTENTES")
    print(len(grupo["submissoes"]))
    print("=" * 50)

    try:

        StorageService.substituir_avaliacao(
            grupo["avaliacao"],
            [
                arquivo["caminho"]
                for arquivo in submissao["arquivos"]
            ],
        )

        print("=" * 50)
        print("ARQUIVOS SALVOS COM SUCESSO")
        print("=" * 50)

        # Remove TODAS as pastas temporárias das versões
        pastas_removidas = set()

        for versao in grupo["submissoes"]:

            if not versao["arquivos"]:
                continue

            pasta_envio = (
                versao["arquivos"][0]["caminho"].parent
            )

            if pasta_envio in pastas_removidas:
                continue

            print(
                f"Removendo pasta temporária: {pasta_envio}"
            )

            FileService.remover_pasta_envio(
                pasta_envio,
            )

            pastas_removidas.add(
                pasta_envio,
            )

    except Exception:

        traceback.print_exc()

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                "❌ Ocorreu um erro ao salvar os arquivos.\n"
                "A revisão não foi removida da fila."
            ),
        )

        return

    await clear_review_messages(
        context=context,
        chat_id=update.effective_chat.id,
    )

    await clear_review_acervo_messages(
        context=context,
        chat_id=update.effective_chat.id,
    )

    sucesso = ReviewQueueService.remover_revisao(
        review_index,
    )

    if not sucesso:

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Esta revisão não existe mais.",
        )

        return

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "✅ Versão aprovada com sucesso!\n\n"
            "A comparação foi concluída."
        ),
    )