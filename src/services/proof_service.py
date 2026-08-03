from pathlib import Path

from services.file_service import FileService
from services.path_service import PathService
from services.name_service import NameService


class ProofService:

    @classmethod
    def obter_paginas(
        cls,
        avaliacao: dict,
    ) -> list[Path]:

        caminho = PathService.gerar_caminho(
            avaliacao,
        )

        nome_avaliacao = (
            NameService.gerar_nome_avaliacao(
                avaliacao,
            )
        )

        pasta = (
            FileService.PROVAS_DIR
            / caminho
            / nome_avaliacao
        )

        if not pasta.exists():

            return []

        paginas = sorted(
            pasta.glob("*")
        )

        return paginas