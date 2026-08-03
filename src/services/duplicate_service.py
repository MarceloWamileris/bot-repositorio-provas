from pathlib import Path

from services.path_service import PathService
from services.name_service import NameService
from services.file_service import FileService


class DuplicateService:

    @classmethod
    def existe(
        cls,
        avaliacao: dict,
    ) -> bool:

        caminho = PathService.gerar_caminho(
            avaliacao,
        )

        diretorio_turno = (
            FileService.PROVAS_DIR / caminho
        )

        nome_avaliacao = (
            NameService.gerar_nome_avaliacao(
                avaliacao,
            )
        )

        pasta_avaliacao = (
            diretorio_turno / nome_avaliacao
        )

        return pasta_avaliacao.exists()