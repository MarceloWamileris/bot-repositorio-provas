from pathlib import Path


class PathService:

    @staticmethod
    def gerar_caminho(avaliacao: dict) -> Path:

        periodo = avaliacao["periodo"]

        disciplina = (
            f'{avaliacao["nome_disciplina"]} '
            f'({avaliacao["codigo_disciplina"]})'
        )

        professor = avaliacao["nome_professor"]

        semestre = (
            f'{avaliacao["ano"]}-'
            f'{avaliacao["semestre"]}'
        )

        turno = avaliacao["turno"]

        return Path(
            periodo,
            disciplina,
            professor,
            semestre,
            turno,
        )