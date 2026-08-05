from telegram import Update
from telegram.ext import ContextTypes

from services.review_queue_service import (
    ReviewQueueService,
)

from bot.keyboards.review_details_keyboard import (
    review_details_keyboard,
)


async def enviar_detalhes_revisao(
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE,
    grupo: dict,
    mensagem: str | None = None,
    message_id: int | None = None,
):

    if message_id is not None:
        try:
            await context.bot.delete_message(
                chat_id=chat_id,
                message_id=message_id,
            )
        except Exception:
            pass

    avaliacao = grupo["avaliacao"]

    texto = ""

    if mensagem:
        texto += mensagem + "\n\n"

    if grupo["tipo"] == "comparacao":

        texto += (
            "📚 Comparação de provas\n\n"
            f"Disciplina: {avaliacao['codigo_disciplina']}\n"
            f"Professor: {avaliacao['nome_professor']}\n"
            f"Ano: {avaliacao['ano']}\n"
            f"Semestre: {avaliacao['semestre']}\n"
            f"Turno: {avaliacao['turno']}\n"
            f"Avaliação: {avaliacao['avaliacao']}\n\n"
            "⚠️ Já existe uma prova desta avaliação no acervo.\n\n"
            "Selecione uma versão enviada pelo aluno para compará-la "
            "com a prova atualmente armazenada.\n\n"
            f"Versões enviadas: {grupo['quantidade']}\n\n"
            "⬇️ Selecione uma versão:"
        )

    else:

        texto += (
            "📄 Revisão selecionada\n\n"
            f"Disciplina: {avaliacao['codigo_disciplina']}\n"
            f"Professor: {avaliacao['nome_professor']}\n"
            f"Ano: {avaliacao['ano']}\n"
            f"Semestre: {avaliacao['semestre']}\n"
            f"Turno: {avaliacao['turno']}\n"
            f"Avaliação: {avaliacao['avaliacao']}\n\n"
            f"Versões pendentes: {grupo['quantidade']}\n\n"
            "⬇️ Selecione uma versão:"
        )

    await context.bot.send_message(
        chat_id=chat_id,
        text=texto,
        reply_markup=review_details_keyboard(
            grupo,
        ),
    )


async def callback_review_details(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    indice = int(
        query.data.removeprefix(
            "review:"
        )
    )

    revisoes = ReviewQueueService.listar()

    grupo = next(
        (
            revisao
            for revisao in revisoes
            if revisao["indice"] == indice
        ),
        None,
    )

    if grupo is None:

        await query.edit_message_text(
            text=(
                "⚠️ Esta revisão não está mais disponível."
            )
        )

        return

    await enviar_detalhes_revisao(
        chat_id=update.effective_chat.id,
        context=context,
        grupo=grupo,
        message_id=query.message.message_id,
    )