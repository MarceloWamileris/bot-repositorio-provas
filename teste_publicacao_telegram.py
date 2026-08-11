import asyncio
from pathlib import Path

from services.telegram_publication_service import (
    TelegramPublicationService,
)


avaliacao = {
    "nome_disciplina": "Interface Homem-Máquina",
    "codigo_disciplina": "1IHM",
    "nome_professor": "André Henrique Pedrosa Neves",
    "ano": "2023",
    "semestre": "1",
    "turno": "Manhã",
    "avaliacao": "AV1",
}


diretorio = Path(
    r"D:\RepositorioProvas\Provas\Primeiro Período"
    r"\Interface Homem-Máquina (1IHM)"
    r"\André Henrique Pedrosa Neves"
    r"\2023-1"
    r"\Manhã"
    r"\AV1"
)


async def main():

    await TelegramPublicationService.publicar_prova_teste(
        avaliacao,
        diretorio,
    )


asyncio.run(main())