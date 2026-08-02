from pathlib import Path
from uuid import uuid4

from config.settings import settings


class FileService:

    TEMP_DIR = settings.ARQUIVOS_DIR / "temp"

    @classmethod
    def criar_pasta_envio(cls, user_id: int) -> Path:

        pasta_usuario = cls.TEMP_DIR / str(user_id)

        pasta_envio = pasta_usuario / str(uuid4())

        pasta_envio.mkdir(
            parents=True,
            exist_ok=True,
        )

        return pasta_envio