from pathlib import Path

from services.path_service import PathService
from services.file_service import FileService
from services.name_service import NameService


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

    @classmethod
    def gerar_destino_disponivel(
        cls,
        diretorio: Path,
        nome_arquivo: str,
    ) -> Path:

        destino = diretorio / nome_arquivo

        if not destino.exists():

            return destino

        nome = destino.stem
        extensao = destino.suffix

        contador = 2

        while True:

            novo_destino = (
                diretorio / f"{nome} ({contador}){extensao}"
            )

            if not novo_destino.exists():

                return novo_destino

            contador += 1

    @classmethod
    def armazenar_arquivo(
        cls,
        avaliacao: dict,
        arquivo_original: Path,
    ) -> Path:

        diretorio = cls.preparar_destino(
            avaliacao,
        )

        nome_arquivo = NameService.gerar_nome(
            avaliacao,
            arquivo_original,
        )

        destino = cls.gerar_destino_disponivel(
            diretorio,
            nome_arquivo,
        )

        FileService.mover_arquivo(
            arquivo_original,
            destino,
        )

        return destino