from pathlib import Path
from dotenv import load_dotenv
import os


class Settings:

    def __init__(self):

        load_dotenv()

        self.BOT_TOKEN = os.getenv(
            "BOT_TOKEN"
        )

        self.ADMIN_ID = int(
            os.getenv("ADMIN_ID")
        )

        self.BASE_STORAGE = Path(
            "D:/RepositorioProvas"
        )

        self.TEMP_PATH = (
            self.BASE_STORAGE / "Temp"
        )

        self.PROVAS_PATH = (
            self.BASE_STORAGE / "Provas"
        )

        self.BACKUP_PATH = (
            self.BASE_STORAGE / "Backup"
        )

        self.LOG_PATH = (
            self.BASE_STORAGE / "Logs"
        )


settings = Settings()