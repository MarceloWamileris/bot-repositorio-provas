from telegram import Update
from telegram.ext import ContextTypes

from services.duplicate_service import (
    DuplicateService,
)
from services.proof_service import (
    ProofService,
)
from services.review_queue_service import (
    ReviewQueueService,
)
from services.review_service import (
    ReviewService,
)
from services.session_service import (
    SessionService,
)


class EvaluationService:

    @classmethod
    async def finalizar(
        cls,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        avaliacao = context.user_data["avaliacao"]

        arquivos = context.user_data.get(
            "arquivos",
            [],
        )

        if DuplicateService.existe(
            avaliacao,
        ):

            prova_acervo = ProofService.obter_prova(
                avaliacao,
            )

            await ReviewService.iniciar(
                update,
                context,
                avaliacao,
                prova_acervo,
            )

            return "duplicado"

        ReviewQueueService.adicionar(
            usuario_id=update.effective_user.id,
            avaliacao=avaliacao,
            arquivos=arquivos,
        )

        SessionService.finalizar(
            context,
        )

        return "fila"