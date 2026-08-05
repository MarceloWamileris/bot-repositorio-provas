from pathlib import Path
import shutil

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

        diretorio_turno = FileService.criar_diretorio_provas(
            caminho,
        )

        nome_avaliacao = (
            NameService.gerar_nome_avaliacao(
                avaliacao,
            )
        )

        diretorio_avaliacao = (
            diretorio_turno
            / nome_avaliacao
        )

        diretorio_avaliacao.mkdir(
            parents=True,
            exist_ok=True,
        )

        return diretorio_avaliacao

    @classmethod
    def gerar_destino_disponivel(
        cls,
        diretorio: Path,
        extensao: str,
    ) -> Path:

        arquivos = [
            arquivo
            for arquivo in diretorio.iterdir()
            if arquivo.is_file()
        ]

        contador = len(arquivos) + 1

        return (
            diretorio
            / f"{contador:02d}{extensao}"
        )

    @classmethod
    def armazenar_arquivo(
        cls,
        avaliacao: dict,
        arquivo_original: Path,
    ) -> Path:

        diretorio = cls.preparar_destino(
            avaliacao,
        )

        destino = cls.gerar_destino_disponivel(
            diretorio,
            arquivo_original.suffix.lower(),
        )

        FileService.mover_arquivo(
            arquivo_original,
            destino,
        )

        return destino

    @classmethod
    def substituir_avaliacao(
        cls,
        avaliacao: dict,
        arquivos: list[Path],
    ):
        """
        Substitui completamente uma avaliação existente
        pelos arquivos aprovados na comparação.
        """

        diretorio = cls.preparar_destino(
            avaliacao,
        )

        if diretorio.exists():

            shutil.rmtree(
                diretorio,
            )

        diretorio.mkdir(
            parents=True,
            exist_ok=True,
        )

        for indice, arquivo in enumerate(
            arquivos,
            start=1,
        ):

            destino = (
                diretorio
                / f"{indice:02d}{arquivo.suffix.lower()}"
            )

            FileService.mover_arquivo(
                arquivo,
                destino,
            )

        return diretorio