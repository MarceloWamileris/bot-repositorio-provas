from pathlib import Path


class NameService:

    @classmethod
    def gerar_nome(
        cls,
        avaliacao: dict,
        arquivo_original: Path,
    ) -> str:

        extensao = arquivo_original.suffix.lower()

        tipo = avaliacao["avaliacao"]

        if tipo == "AVS":

            vinculada = avaliacao["avaliacao_vinculada"]

            return f"AVS ({vinculada}){extensao}"

        return f"{tipo}{extensao}"