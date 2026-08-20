from config.settings import settings
from config.logging_config import configurar_logging

from bot.telegram_bot import TelegramBot

from services.review_queue_storage_service import (
    ReviewQueueStorageService,
)


def main():

    configurar_logging()

    ReviewQueueStorageService.carregar()

    bot = TelegramBot()

    bot.iniciar()


if __name__ == "__main__":

    main()