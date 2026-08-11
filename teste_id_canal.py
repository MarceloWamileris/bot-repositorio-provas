import asyncio

from telegram import Bot

from src.config.settings import settings

CHAT_ID_CANAL = -1004341486454


async def main():

    bot = Bot(
        token=settings.BOT_TOKEN,
    )

    print("=" * 50)
    print("TESTE DE PUBLICAÇÃO NO CANAL")
    print("=" * 50)

    mensagem = await bot.send_message(
        chat_id=CHAT_ID_CANAL,
        text="🤖 Teste de publicação realizado pelo bot.",
    )

    print("PUBLICAÇÃO REALIZADA!")
    print(f"ID da mensagem: {mensagem.message_id}")

    print("=" * 50)


if __name__ == "__main__":

    asyncio.run(main())