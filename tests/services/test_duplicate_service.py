from pathlib import Path

from services.duplicate_service import DuplicateService


avaliacao = {
    "periodo": "Primeiro Período",

    "codigo_disciplina": "1FAC",
    "nome_disciplina": "Fundamentos de Algoritmos de Computação",

    "nome_professor": "Claudia Ferlin",

    "ano": 2026,
    "semestre": 1,

    "turno": "Manhã",

    "avaliacao": "AV2",
    "avaliacao_vinculada": None,
}

arquivo = Path("pagina_1.jpg")

resultado = DuplicateService.existe(
    avaliacao,
    arquivo,
)

print(resultado)