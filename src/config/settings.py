from pathlib import Path
from dotenv import load_dotenv
import os


class Settings:
    def __init__(self):
        load_dotenv()

        self.BOT_TOKEN = os.getenv("BOT_TOKEN")

        self.ARQUIVOS_DIR = Path("D:/RepositorioProvas")


settings = Settings()