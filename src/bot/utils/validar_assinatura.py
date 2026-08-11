from pathlib import Path
from zipfile import ZipFile, BadZipFile

ASSINATURAS = {
    ".pdf": b"%PDF-",
    ".jpg": b"\xFF\xD8\xFF",
    ".jpeg": b"\xFF\xD8\xFF",
    ".png": b"\x89PNG",
}

MARCAS_HEIC = {
    b"heic",
    b"heix",
    b"hevc",
    b"hevx",
    b"mif1",
    b"msf1",
}


def validar_assinatura(caminho: Path) -> bool:

    try:

        with open(caminho, "rb") as arquivo:
            cabecalho = arquivo.read(16)

    except OSError:
        return False

    extensao = caminho.suffix.lower()

    # ------------------------
    # WEBP
    # RIFF....WEBP
    # ------------------------
    if extensao == ".webp":

        return (
            cabecalho.startswith(b"RIFF")
            and cabecalho[8:12] == b"WEBP"
        )

    # ------------------------
    # HEIC
    # ....ftypheic
    # ------------------------
    if extensao == ".heic":

        if cabecalho[4:8] != b"ftyp":
            return False

        return cabecalho[8:12] in MARCAS_HEIC

    # ------------------------
    # DOCX
    # Todo DOCX é um ZIP,
    # mas nem todo ZIP é DOCX.
    # ------------------------
    if extensao == ".docx":

        if not cabecalho.startswith(b"PK"):
            return False

        try:

            with ZipFile(caminho) as arquivo_zip:

                arquivos = arquivo_zip.namelist()

                return any(
                    nome.startswith("word/")
                    for nome in arquivos
                )

        except (BadZipFile, OSError):

            return False

    # ------------------------
    # PDF / JPG / PNG
    # ------------------------
    assinatura = ASSINATURAS.get(extensao)

    # TXT não possui assinatura fixa.
    if assinatura is None:
        return True

    return cabecalho.startswith(assinatura)