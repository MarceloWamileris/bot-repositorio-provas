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

        contador = 1

        while True:

            destino = (
                diretorio
                / f"{contador:02d}{extensao}"
            )

            if not destino.exists():

                return destino

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

        destino = cls.gerar_destino_disponivel(
            diretorio,
            arquivo_original.suffix.lower(),
        )

        FileService.mover_arquivo(
            arquivo_original,
            destino,
        )

        return destino