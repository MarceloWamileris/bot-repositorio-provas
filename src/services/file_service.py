import shutil

from pathlib import Path
from uuid import uuid4

from PIL import Image
from pillow_heif import register_heif_opener

from config.settings import settings


# Habilita suporte ao formato HEIC/HEIF
register_heif_opener()


class FileService:

    TEMP_DIR = settings.TEMP_PATH

    PROVAS_DIR = settings.PROVAS_PATH

    @classmethod
    def criar_pasta_envio(
        cls,
        user_id: int,
    ) -> Path:

        pasta_usuario = cls.TEMP_DIR / str(user_id)

        pasta_envio = pasta_usuario / str(uuid4())

        pasta_envio.mkdir(
            parents=True,
            exist_ok=True,
        )

        return pasta_envio

    @classmethod
    def criar_diretorio_provas(
        cls,
        caminho: Path,
    ) -> Path:

        diretorio = cls.PROVAS_DIR / caminho

        diretorio.mkdir(
            parents=True,
            exist_ok=True,
        )

        return diretorio

    @classmethod
    def mover_arquivo(
        cls,
        origem: Path,
        destino: Path,
    ) -> None:

        shutil.move(
            str(origem),
            str(destino),
        )

    @classmethod
    def remover_pasta_envio(
        cls,
        pasta: Path,
    ) -> None:

        if pasta.exists():

            shutil.rmtree(
                pasta,
            )

    @classmethod
    def converter_heic_para_jpg(
        cls,
        caminho_heic: Path,
    ) -> Path:

        caminho_jpg = caminho_heic.with_suffix(
            ".jpg"
        )

        imagem = Image.open(
            caminho_heic,
        )

        imagem.save(
            caminho_jpg,
            format="JPEG",
            quality=95,
        )

        # Remove o arquivo HEIC original
        caminho_heic.unlink()

        return caminho_jpg