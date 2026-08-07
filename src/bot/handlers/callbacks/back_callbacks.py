from telegram import Update
from telegram.ext import ContextTypes

from messages.select_period import (
    MENSAGEM_PERIODO,
)

from messages.select_disciplina import (
    MENSAGEM_DISCIPLINA,
)

from messages.select_turma_fac import (
    MENSAGEM_TURMA_FAC,
)

from bot.keyboards.period_keyboard import (
    teclado_periodos,
)

from bot.keyboards.disciplina_keyboard import (
    teclado_disciplinas,
)

from bot.keyboards.fac_keyboard import (
    teclado_turma_fac,
)

from messages.select_professor import (
    MENSAGEM_PROFESSOR,
)

from bot.keyboards.teacher_keyboard import (
    teclado_professores,
)

from messages.select_semester import (
    MENSAGEM_SEMESTRE,
)

from bot.keyboards.semester_keyboard import (
    teclado_semestres,
)

async def callback_back_periodo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    avaliacao = context.user_data["avaliacao"]

    avaliacao["periodo"] = None
    avaliacao["codigo_disciplina"] = None
    avaliacao["nome_disciplina"] = None
    avaliacao["turma_fac"] = None
    avaliacao["id_professor"] = None
    avaliacao["nome_professor"] = None

    await query.edit_message_text(
        text=MENSAGEM_PERIODO,
        reply_markup=teclado_periodos(),
    )


async def callback_back_disciplina(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    avaliacao = context.user_data["avaliacao"]

    # limpa somente os dados posteriores
    avaliacao["id_professor"] = None
    avaliacao["nome_professor"] = None

    # Caso especial: FAC
    if avaliacao["codigo_disciplina"] == "1FAC":

        avaliacao["turma_fac"] = None

        await query.edit_message_text(
            text=MENSAGEM_TURMA_FAC,
            reply_markup=teclado_turma_fac(),
        )

        return

    # Fluxo normal
    avaliacao["codigo_disciplina"] = None
    avaliacao["nome_disciplina"] = None

    await query.edit_message_text(
        text=MENSAGEM_DISCIPLINA,
        reply_markup=teclado_disciplinas(
            avaliacao["periodo"],
        ),
    )


async def callback_back_teacher(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    avaliacao = context.user_data["avaliacao"]

    context.user_data["etapa"] = None
    
    # Limpa apenas os dados posteriores ao professor
    avaliacao["ano"] = None
    avaliacao["semestre"] = None
    avaliacao["turno"] = None
    avaliacao["avaliacao"] = None
    avaliacao["avaliacao_vinculada"] = None

    await query.edit_message_text(
        text=MENSAGEM_PROFESSOR,
        reply_markup=teclado_professores(),
    )


async def callback_back_fac(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    avaliacao = context.user_data["avaliacao"]

    # limpa somente a turma
    avaliacao["turma_fac"] = None

    await query.edit_message_text(
        text=MENSAGEM_DISCIPLINA,
        reply_markup=teclado_disciplinas(
            avaliacao["periodo"],
        ),
    )

async def callback_back_semester(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    avaliacao = context.user_data["avaliacao"]

    # volta para a etapa de ano
    context.user_data["etapa"] = "year"

    # limpa apenas os dados posteriores ao ano
    avaliacao["semestre"] = None
    avaliacao["turno"] = None
    avaliacao["avaliacao"] = None
    avaliacao["avaliacao_vinculada"] = None

    from messages.select_year import (
        MENSAGEM_ANO,
    )

    from bot.keyboards.year_keyboard import (
        teclado_ano,
    )

    mensagem = await query.edit_message_text(
        text=MENSAGEM_ANO,
        reply_markup=teclado_ano(),
    )

    context.user_data["mensagem_ano_id"] = (
        mensagem.message_id
    )


async def callback_back_shift(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    avaliacao = context.user_data["avaliacao"]

    # volta para a etapa de semestre
    context.user_data["etapa"] = "semester"

    # limpa somente os dados posteriores
    avaliacao["turno"] = None
    avaliacao["avaliacao"] = None
    avaliacao["avaliacao_vinculada"] = None

    await query.edit_message_text(
        text=MENSAGEM_SEMESTRE,
        reply_markup=teclado_semestres(
            avaliacao["ano"],
        ),
    )


from messages.select_shift import (
    MENSAGEM_TURNO,
)

from bot.keyboards.shift_keyboard import (
    shift_keyboard,
)


async def callback_back_evaluation(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    avaliacao = context.user_data["avaliacao"]

    # volta para a etapa de turno
    context.user_data["etapa"] = "shift"

    # limpa apenas os dados posteriores
    avaliacao["avaliacao"] = None
    avaliacao["avaliacao_vinculada"] = None

    await query.edit_message_text(
        text=MENSAGEM_TURNO,
        reply_markup=shift_keyboard(),
    )


from messages.select_evaluation import (
    MENSAGEM_AVALIACAO,
)

from bot.keyboards.evaluation_keyboard import (
    evaluation_keyboard,
)


async def callback_back_linked_evaluation(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    avaliacao = context.user_data["avaliacao"]

    # volta para a etapa de avaliação
    context.user_data["etapa"] = "evaluation"

    # limpa a avaliação escolhida
    avaliacao["avaliacao"] = None
    avaliacao["avaliacao_vinculada"] = None

    await query.edit_message_text(
        text=MENSAGEM_AVALIACAO,
        reply_markup=evaluation_keyboard(),
    )