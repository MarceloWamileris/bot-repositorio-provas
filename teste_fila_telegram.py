from pathlib import Path

from services.telegram_publication_queue_service import (
    TelegramPublicationQueueService,
)


avaliacao_1 = {
    "codigo_disciplina": "1IHM",
    "nome_disciplina": "Interface Homem-Máquina",
    "nome_professor": "André Henrique Pedrosa Neves",
    "ano": "2023",
    "semestre": "1",
    "turno": "Manhã",
    "avaliacao": "AV1",
}


arquivos_1 = [
    Path(
        r"D:\RepositorioProvas\Provas\Primeiro Período"
        r"\Interface Homem-Máquina (1IHM)"
        r"\André Henrique Pedrosa Neves"
        r"\2023-1\Manhã\AV1\01.jpg"
    )
]


avaliacao_2 = {
    "codigo_disciplina": "1MAB",
    "nome_disciplina": "Matemática Básica",
    "nome_professor": "Professor de Teste",
    "ano": "2026",
    "semestre": "1",
    "turno": "Noite",
    "avaliacao": "AV2",
}


arquivos_2 = [
    Path(
        r"D:\RepositorioProvas\Provas\Primeiro Período"
        r"\Matemática Básica (1MAB)"
        r"\Professor de Teste"
        r"\2026-1\Noite\AV2\01.jpg"
    )
]


TelegramPublicationQueueService.adicionar(
    avaliacao_1,
    arquivos_1,
)

TelegramPublicationQueueService.adicionar(
    avaliacao_2,
    arquivos_2,
)


publicacoes = (
    TelegramPublicationQueueService.listar()
)

print("=" * 50)
print("FILA DE PUBLICAÇÕES")
print("=" * 50)

print(
    f"Total de publicações: "
    f"{len(publicacoes)}"
)

for indice, publicacao in enumerate(
    publicacoes,
    start=1,
):

    print(
        f"\nPUBLICAÇÃO {indice}"
    )

    print(
        f"Disciplina: "
        f"{publicacao['avaliacao']['nome_disciplina']}"
    )

    print(
        f"Avaliação: "
        f"{publicacao['avaliacao']['avaliacao']}"
    )

    print(
        f"Arquivos: "
        f"{publicacao['arquivos']}"
    )

print("=" * 50)
