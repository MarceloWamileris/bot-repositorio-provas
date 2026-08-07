from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from bot.handlers.start_handler import start
from bot.handlers.review_list_handler import (
    listar_revisoes,
)
from bot.handlers.file_handler import receber_arquivo
from bot.handlers.upload_handler import upload
from bot.handlers.year_handler import receber_ano

from bot.handlers.callbacks.menu_callbacks import (
    callback_enviar,
    callback_consultar,
    callback_ajuda,
)

from bot.handlers.callbacks.finish_callbacks import (
    callback_finalizar,
)

from bot.handlers.callbacks.periodo_callbacks import (
    callback_periodo,
)

from bot.handlers.callbacks.disciplina_callbacks import (
    callback_disciplina,
)

from bot.handlers.callbacks.teacher_callbacks import (
    callback_teacher,
)

from bot.handlers.callbacks.semester_callbacks import (
    callback_semester,
)

from bot.handlers.callbacks.shift_callbacks import (
    callback_shift,
)

from bot.handlers.callbacks.evaluation_callbacks import (
    callback_evaluation,
)

from bot.handlers.callbacks.linked_evaluation_callbacks import (
    callback_linked_evaluation,
)

from bot.handlers.callbacks.review_admin_callbacks import (
    callback_review_details,
)

from bot.handlers.callbacks.review_list_callbacks import (
    callback_review_list,
)

from bot.handlers.callbacks.submission_admin_callbacks import (
    callback_submission_details,
    callback_submission_files,
    callback_submission_approve,
    callback_submission_reject,
    callback_submission_next,
    callback_submission_previous,
)

from bot.handlers.callbacks.submission_compare_callbacks import (
    callback_compare_next,
    callback_compare_previous,
    callback_compare_reject,
    callback_compare_approve,
)

from bot.handlers.callbacks.review_callbacks import (
    callback_review_request,
    callback_review_cancel,
)

from bot.handlers.callbacks.fac_callbacks import (
    callback_fac,
)

from bot.handlers.callbacks.back_callbacks import (
    callback_back_periodo,
    callback_back_disciplina,
    callback_back_teacher,
    callback_back_semester,
    callback_back_shift,
    callback_back_evaluation,
    callback_back_linked_evaluation,
    callback_back_fac,
)

def register_commands(application: Application):

    application.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    application.add_handler(
        CommandHandler(
            "revisoes",
            listar_revisoes,
        )
    )


def register_callbacks(application: Application):

    application.add_handler(
        CallbackQueryHandler(
            callback_enviar,
            pattern="^enviar$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_consultar,
            pattern="^consultar$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_ajuda,
            pattern="^ajuda$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            upload,
            pattern="^upload$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_finalizar,
            pattern="^finalizar_envio$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_periodo,
            pattern="^periodo:",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_back_periodo,
            pattern="^voltar:periodo$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_disciplina,
            pattern="^disciplina:",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_back_disciplina,
            pattern="^voltar:disciplina$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_back_fac,
            pattern="^voltar:fac$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_fac,
            pattern="^fac:",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_teacher,
            pattern="^professor:",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_semester,
            pattern="^semestre:",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_back_semester,
            pattern="^voltar:ano$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_back_teacher,
            pattern="^voltar:professor$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_shift,
            pattern="^turno:",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_back_shift,
            pattern="^voltar:semestre$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_evaluation,
            pattern="^avaliacao:",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_back_evaluation,
            pattern="^voltar:turno$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_linked_evaluation,
            pattern="^vinculada:",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_back_linked_evaluation,
            pattern="^voltar:avaliacao$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_review_details,
            pattern=r"^review:\d+$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_review_list,
            pattern=r"^review:list$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_submission_details,
            pattern=r"^submission:\d+:\d+$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_submission_files,
            pattern=r"^submission:files:\d+:\d+$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_submission_approve,
            pattern=r"^submission:approve:\d+:\d+$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_submission_reject,
            pattern=r"^submission:reject:\d+:\d+$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_review_request,
            pattern="^review:request$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            callback_review_cancel,
            pattern="^review:cancel$",
        )
    )

    application.add_handler(
    CallbackQueryHandler(
            callback_submission_next,
            pattern=r"^submission:next:\d+:\d+$",
        )
    )

    application.add_handler(
    CallbackQueryHandler(
            callback_submission_previous,
            pattern=r"^submission:previous:\d+:\d+$",
        )
    )

    application.add_handler(
    CallbackQueryHandler(
        callback_compare_next,
        pattern=r"^compare:next:\d+:\d+$",
        )
    )

    application.add_handler(
    CallbackQueryHandler(
        callback_compare_previous,
        pattern=r"^compare:previous:\d+:\d+$",
        )
    )

    application.add_handler(
    CallbackQueryHandler(
        callback_compare_reject,
        pattern=r"^compare:reject:\d+:\d+$",
        )
    )

    application.add_handler(
    CallbackQueryHandler(
        callback_compare_approve,
        pattern=r"^compare:approve:\d+:\d+$",
        )
    )


def register_messages(application: Application):

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            receber_ano,
        )
    )

    application.add_handler(
        MessageHandler(
            filters.PHOTO | filters.Document.PDF,
            receber_arquivo,
        )
    )


def register_handlers(application: Application):

    register_commands(application)

    register_callbacks(application)

    register_messages(application)



