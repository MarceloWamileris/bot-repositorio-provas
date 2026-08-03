from services.path_service import PathService
from services.file_service import FileService


avaliacao = {
    "periodo": "Primeiro Período",

    "codigo_disciplina": "1IHM",
    "nome_disciplina": "Interface Homem-Máquina",

    "nome_professor": "Maria Cláudia",

    "ano": 2026,
    "semestre": 1,

    "turno": "Noite",
}

caminho = PathService.gerar_caminho(avaliacao)

diretorio = FileService.criar_diretorio_provas(caminho)

print(diretorio)