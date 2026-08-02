from pathlib import Path

from config.settings import settings


class FileService:

    TEMP_DIR = settings.ARQUIVOS_DIR / "temp"

    @classmethod
    def criar_pasta_usuario(cls, user_id: int) -> Path:

        pasta = cls.TEMP_DIR / str(user_id)

        pasta.mkdir(
            parents=True,
            exist_ok=True,
        )

        return pasta