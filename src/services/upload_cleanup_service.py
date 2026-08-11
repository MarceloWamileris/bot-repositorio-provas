import json
import time
from pathlib import Path
from threading import Lock

from services.file_service import (
    FileService,
)


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

        print("=" * 50)
        print("LIMPANDO EXPIRADOS")
        print("=" * 50)

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

            TTL = 3600  # 1 minuto para teste
            # TTL = 3600  # 1 hora em produção

            usuarios_expirados = []

            for usuario_id, dados in status.items():

                idade = (
                    agora
                    - dados["criado_em"]
                )

                print("-" * 40)
                print(
                    f"Usuário: {usuario_id}"
                )
                print(
                    f"Pasta: {dados['pasta']}"
                )
                print(
                    f"Idade: {idade} segundos"
                )

                if idade > TTL:

                    print(
                        ">>> EXPIRADO <<<"
                    )

                    usuarios_expirados.append(
                        usuario_id,
                    )

                else:

                    print(
                        "Ainda válido."
                    )

            print("=" * 50)
            print("UPLOADS EXPIRADOS:")
            print(usuarios_expirados)
            print("=" * 50)

            for usuario_id in usuarios_expirados:

                pasta = Path(
                    status[usuario_id]["pasta"]
                )

                print(
                    f"Removendo pasta: {pasta}"
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

                print("=" * 50)
                print(
                    "STATUS.JSON ATUALIZADO"
                )
                print(status)
                print("=" * 50)

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

            print("=" * 50)
            print("UPLOAD REGISTRADO")
            print(status)
            print("=" * 50)

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

            print("=" * 50)
            print(
                "UPLOAD REMOVIDO DO STATUS.JSON"
            )
            print(status)
            print("=" * 50)

    @classmethod
    def _garantir_status(cls):

        print("=" * 50)
        print("GARANTINDO STATUS.JSON")
        print(
            "CAMINHO:",
            cls.STATUS_FILE.resolve(),
        )
        print("=" * 50)

        cls.STATUS_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not cls.STATUS_FILE.exists():

            print(
                "CRIANDO STATUS.JSON"
            )

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

        else:

            print(
                "STATUS.JSON JÁ EXISTE"
            )

