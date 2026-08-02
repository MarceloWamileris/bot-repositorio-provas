from pathlib import Path

from PIL import Image
import pytesseract


CAMINHO_IMAGEM = (
    Path(__file__).parent
    / "imagens"
    / "prova_real.png"
)


def executar_ocr(
    imagem: Image.Image,
    titulo: str,
):

    print(f"\n========== {titulo} ==========\n")

    texto = pytesseract.image_to_string(
        imagem,
        lang="por",
    )

    print(texto)

    print("\n==============================\n")


imagem = Image.open(CAMINHO_IMAGEM)

imagem_cinza = imagem.convert("L")

imagem_pb = imagem_cinza.point(
    lambda pixel: 255 if pixel > 150 else 0,
    mode="1",
)

# NOVO EXPERIMENTO
imagem_2x = imagem.resize(
    (
        imagem.width * 2,
        imagem.height * 2,
    ),
    Image.Resampling.LANCZOS,
)

executar_ocr(
    imagem,
    "IMAGEM ORIGINAL",
)

executar_ocr(
    imagem_cinza,
    "ESCALA DE CINZA",
)

executar_ocr(
    imagem_pb,
    "PRETO E BRANCO",
)

executar_ocr(
    imagem_2x,
    "RESOLUÇÃO 2X",
)