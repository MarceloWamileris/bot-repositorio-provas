from pathlib import Path

from services.storage_service import StorageService


diretorio = Path("D:/RepositorioProvas/Teste")

diretorio.mkdir(
    parents=True,
    exist_ok=True,
)

for nome in [
    "AV1.pdf",
    "AV1 (2).pdf",
    "AV1 (3).pdf",
]:
    (diretorio / nome).touch(exist_ok=True)

destino = StorageService.gerar_destino_disponivel(
    diretorio,
    "AV1.pdf",
)

print(destino)