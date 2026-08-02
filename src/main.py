from config.settings import settings
from bot.telegram_bot import TelegramBot


def main():
    bot = TelegramBot()
    bot.iniciar()


if __name__ == "__main__":
    main()