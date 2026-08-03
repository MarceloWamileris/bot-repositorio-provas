class NameService:

    @classmethod
    def gerar_nome_avaliacao(
        cls,
        avaliacao: dict,
    ) -> str:

        tipo = avaliacao["avaliacao"]

        if tipo == "AVS":

            vinculada = avaliacao["avaliacao_vinculada"]

            return f"AVS ({vinculada})"

        return tipo