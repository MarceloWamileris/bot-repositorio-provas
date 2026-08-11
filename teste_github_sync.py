from services.github_sync_service import GitHubSyncService


avaliacao = {
    "periodo": "Primeiro Período",
    "codigo_disciplina": "1FAC",
    "nome_disciplina": "Fundamentos de Algoritmos de Computação",
    "id_professor": 1,
    "nome_professor": "Professor Teste",
    "ano": 2026,
    "semestre": 1,
    "turno": "noite",
    "avaliacao": "AV1",
    "avaliacao_vinculada": None,
    "turma_fac": "FAC-A",
}


GitHubSyncService.sincronizar(
    avaliacao,
    "adicionar",
)