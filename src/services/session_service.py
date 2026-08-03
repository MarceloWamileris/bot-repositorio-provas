class SessionService:

    @classmethod
    def finalizar(
        cls,
        context,
    ):

        context.user_data["etapa"] = None