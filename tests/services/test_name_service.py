from pathlib import Path

from services.name_service import NameService


casos = [
    (
        {
            "avaliacao": "AV1",
            "avaliacao_vinculada": None,
        },
        Path("prova.pdf"),
    ),
    (
        {
            "avaliacao": "AV2",
            "avaliacao_vinculada": None,
        },
        Path("foto.jpg"),
    ),
    (
        {
            "avaliacao": "AVF",
            "avaliacao_vinculada": None,
        },
        Path("imagem.png"),
    ),
    (
        {
            "avaliacao": "AVS",
            "avaliacao_vinculada": "AV1",
        },
        Path("arquivo.jpeg"),
    ),
    (
        {
            "avaliacao": "AVS",
            "avaliacao_vinculada": "AV2",
        },
        Path("documento.pdf"),
    ),
]

for avaliacao, arquivo in casos:

    print(
        NameService.gerar_nome(
            avaliacao,
            arquivo,
        )
    )