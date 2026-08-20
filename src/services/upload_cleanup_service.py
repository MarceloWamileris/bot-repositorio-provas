import json
import logging
import time
from pathlib import Path
from threading import Lock

from services.file_service import (
    FileService,
)

logger = logging.getLogger(__name__)


class UploadCleanupService:

    STATUS_FILE = (
        FileService.TEMP_DIR / "status.json"
    )

    # Impede que duas operações alterem o
    # status.json simultaneamente.
    _lock = Lock()

    @classmethod
    async def limpar_expirados(
        cls,
        context=None,
    ):

        with cls._lock:

            cls._garantir_status()

            with open(
                cls.STATUS_FILE,
                "r",
                encoding="utf-8",
            ) as arquivo:

                status = json.load(
                    arquivo,
                )

            agora = int(
                time.time()
            )

            TTL = 3600  
            # TTL = 3600  # 1 hora em produção

            usuarios_expirados = []

            for usuario_id, dados in status.items():

                idade = (
                    agora
                    - dados["criado_em"]
                )

                if idade > TTL:

                    usuarios_expirados.append(
                        usuario_id,
                    )

            if usuarios_expirados:

                logger.info(
                    f"Removendo {len(usuarios_expirados)} "
                    f"upload(s) expirado(s): "
                    f"{usuarios_expirados}"
                )

            for usuario_id in usuarios_expirados:

                pasta = Path(
                    status[usuario_id]["pasta"]
                )

                FileService.remover_pasta_envio(
                    pasta,
                )

                status.pop(
                    usuario_id,
                    None,
                )

            if usuarios_expirados:

                with open(
                    cls.STATUS_FILE,
                    "w",
                    encoding="utf-8",
                ) as arquivo:

                    json.dump(
                        status,
                        arquivo,
                        indent=4,
                        ensure_ascii=False,
                    )

    @classmethod
    def registrar_upload(
        cls,
        usuario_id: int,
        pasta: Path,
    ):

        with cls._lock:

            cls._garantir_status()

            with open(
                cls.STATUS_FILE,
                "r",
                encoding="utf-8",
            ) as arquivo:

                status = json.load(
                    arquivo,
                )

            status[str(usuario_id)] = {
                "pasta": str(pasta),
                "criado_em": int(
                    time.time()
                ),
            }

            with open(
                cls.STATUS_FILE,
                "w",
                encoding="utf-8",
            ) as arquivo:

                json.dump(
                    status,
                    arquivo,
                    indent=4,
                    ensure_ascii=False,
                )

    @classmethod
    def finalizar_upload(
        cls,
        usuario_id: int,
    ):

        with cls._lock:

            cls._garantir_status()

            with open(
                cls.STATUS_FILE,
                "r",
                encoding="utf-8",
            ) as arquivo:

                status = json.load(
                    arquivo,
                )

            status.pop(
                str(usuario_id),
                None,
            )

            with open(
                cls.STATUS_FILE,
                "w",
                encoding="utf-8",
            ) as arquivo:

                json.dump(
                    status,
                    arquivo,
                    indent=4,
                    ensure_ascii=False,
                )

    @classmethod
    def _garantir_status(cls):

        cls.STATUS_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not cls.STATUS_FILE.exists():

            with open(
                cls.STATUS_FILE,
                "w",
                encoding="utf-8",
            ) as arquivo:

                json.dump(
                    {},
                    arquivo,
                    indent=4,
                    ensure_ascii=False,
                )

