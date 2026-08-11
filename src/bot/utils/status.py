from datetime import datetime, timedelta
from pathlib import Path
import json
import shutil


NOME_STATUS = "status.json"

TTL_HORAS = 1


def criar_status(pasta: Path):

    caminho = pasta / NOME_STATUS

    agora = datetime.now().isoformat()

    dados = {
        "criado_em": agora,
        "ultima_atualizacao": agora,
    }

    with open(
        caminho,
        "w",
        encoding="utf-8",
    ) as arquivo:

        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False,
        )


def atualizar_status(pasta: Path):

    caminho = pasta / NOME_STATUS

    if not caminho.exists():
        return

    with open(
        caminho,
        "r",
        encoding="utf-8",
    ) as arquivo:

        dados = json.load(arquivo)

    dados["ultima_atualizacao"] = (
        datetime.now().isoformat()
    )

    with open(
        caminho,
        "w",
        encoding="utf-8",
    ) as arquivo:

        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False,
        )


def ler_status(pasta: Path):

    caminho = pasta / NOME_STATUS

    if not caminho.exists():
        return None

    with open(
        caminho,
        "r",
        encoding="utf-8",
    ) as arquivo:

        return json.load(arquivo)


def limpar_pastas_expiradas(
    pasta_temp: Path,
):

    agora = datetime.now()

    for pasta in pasta_temp.iterdir():

        if not pasta.is_dir():
            continue

        status = ler_status(pasta)

        if status is None:

            shutil.rmtree(
                pasta,
                ignore_errors=True,
            )

            continue

        try:

            ultima_atualizacao = datetime.fromisoformat(
                status["ultima_atualizacao"]
            )

        except Exception:

            shutil.rmtree(
                pasta,
                ignore_errors=True,
            )

            continue

        if (
            agora - ultima_atualizacao
            >= timedelta(hours=TTL_HORAS)
        ):

            shutil.rmtree(
                pasta,
                ignore_errors=True,
            )