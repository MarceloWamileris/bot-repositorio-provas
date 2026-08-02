from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from bot.handlers.start_handler import start
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


def register_commands(application: Application):

    application.add_handler(
        CommandHandler(
            "start",
            start,
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
            callback_disciplina,
            pattern="^disciplina:",
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
            callback_shift,
            pattern="^turno:",
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
            callback_linked_evaluation,
            pattern="^vinculada:",
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