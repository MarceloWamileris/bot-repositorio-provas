class AdminReviewSessionService:

    _mensagens = {}

    @classmethod
    def adicionar_mensagem(
        cls,
        chat_id: int,
        message_id: int,
    ):
        ...
    
    @classmethod
    async def limpar(
        cls,
        bot,
        chat_id: int,
    ):
        ...