from services.storage_service import StorageService


avaliacao = {
    "periodo": "Terceiro Período",

    "codigo_disciplina": "3PBD",
    "nome_disciplina": "Banco de Dados",

    "nome_professor": "André",

    "ano": 2025,
    "semestre": 2,

    "turno": "Tarde",

    "avaliacao": "AV2",
    "avaliacao_vinculada": None,
}

diretorio = StorageService.preparar_destino(avaliacao)

print(diretorio)