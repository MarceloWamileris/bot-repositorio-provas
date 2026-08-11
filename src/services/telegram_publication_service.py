from pathlib import Path

from telegram import Bot

from config.settings import settings


class TelegramPublicationService:

    @classmethod
    async def publicar_prova(
        cls,
        avaliacao: dict,
        arquivos: list[Path],
    ):

        bot = Bot(
            token=settings.BOT_TOKEN,
        )

        # --------------------------------------------------
        # Mensagem da avaliação
        # --------------------------------------------------

        texto = (
            "📚 Nova avaliação disponível\n\n"
            f"📘 Disciplina: "
            f"{avaliacao['nome_disciplina']} "
            f"({avaliacao['codigo_disciplina']})\n\n"
            f"👨‍🏫 Professor: "
            f"{avaliacao['nome_professor']}\n\n"
            f"📅 Ano/Semestre: "
            f"{avaliacao['ano']}-"
            f"{avaliacao['semestre']}\n\n"
            f"🌙 Turno: "
            f"{avaliacao['turno']}\n\n"
            f"📝 Avaliação: "
            f"{avaliacao['avaliacao']}"
        )

        # --------------------------------------------------
        # Exceção da 1FAC
        # --------------------------------------------------

        if (
            avaliacao["codigo_disciplina"]
            == "1FAC"
        ):

            texto += (
                "\n\n"
                f"👥 Turma: "
                f"{avaliacao['turma_fac']}"
            )

        # --------------------------------------------------
        # Exceção da AVS
        # --------------------------------------------------

        if (
            avaliacao["avaliacao"]
            == "AVS"
        ):

            texto += (
                "\n\n"
                f"🔗 Avaliação vinculada: "
                f"{avaliacao['avaliacao_vinculada']}"
            )

        # --------------------------------------------------
        # Publica a mensagem
        # --------------------------------------------------

        mensagem = await bot.send_message(
            chat_id=settings.TELEGRAM_CHANNEL_ID,
            text=texto,
        )

        print("=" * 50)
        print("PUBLICAÇÃO NO TELEGRAM")
        print("=" * 50)
        print("PUBLICAÇÃO REALIZADA!")
        print(
            f"ID da mensagem: "
            f"{mensagem.message_id}"
        )
        print("=" * 50)

        # --------------------------------------------------
        # Publica os arquivos
        # --------------------------------------------------

        for arquivo in sorted(arquivos):

            with arquivo.open("rb") as arquivo_aberto:

                if arquivo.suffix.lower() in (
                    ".jpg",
                    ".jpeg",
                    ".png",
                ):

                    mensagem = await bot.send_photo(
                        chat_id=settings.TELEGRAM_CHANNEL_ID,
                        photo=arquivo_aberto,
                    )

                else:

                    mensagem = await bot.send_document(
                        chat_id=settings.TELEGRAM_CHANNEL_ID,
                        document=arquivo_aberto,
                    )

            print(
                f"Arquivo publicado: "
                f"{arquivo.name} "
                f"(ID: {mensagem.message_id})"
            )