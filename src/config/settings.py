from dotenv import load_dotenv
import os

class Settings:
    def __init__(self):
        load_dotenv()
        self.BOT_TOKEN = os.getenv("BOT_TOKEN")


settings = Settings()