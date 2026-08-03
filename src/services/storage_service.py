from pathlib import Path

from services.path_service import PathService
from services.file_service import FileService


class StorageService:

    @classmethod
    def preparar_destino(
        cls,
        avaliacao: dict,
    ) -> Path:

        caminho = PathService.gerar_caminho(
            avaliacao,
        )

        diretorio = FileService.criar_diretorio_provas(
            caminho,
        )

        return diretorio