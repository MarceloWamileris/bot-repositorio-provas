import asyncio

from telegram.error import TimedOut


class TelegramService:

    MAX_TENTATIVAS = 3

    @classmethod
    async def send_document(
        cls,
        bot,
        **kwargs,
    ):

        for tentativa in range(cls.MAX_TENTATIVAS):

            try:

                if hasattr(
                    kwargs["document"],
                    "seek",
                ):

                    kwargs["document"].seek(0)

                return await bot.send_document(
                    **kwargs,
                )

            except TimedOut:

                print(
                    f"[Telegram] Timeout "
                    f"(tentativa {tentativa + 1})"
                )

                if tentativa == cls.MAX_TENTATIVAS - 1:

                    raise

                await asyncio.sleep(
                    tentativa + 1
                )

    @classmethod
    async def send_photo(
        cls,
        bot,
        **kwargs,
    ):

        for tentativa in range(cls.MAX_TENTATIVAS):

            try:

                if hasattr(
                    kwargs["photo"],
                    "seek",
                ):

                    kwargs["photo"].seek(0)

                return await bot.send_photo(
                    **kwargs,
                )

            except TimedOut:

                print(
                    f"[Telegram] Timeout "
                    f"(tentativa {tentativa + 1})"
                )

                if tentativa == cls.MAX_TENTATIVAS - 1:

                    raise

                await asyncio.sleep(
                    tentativa + 1
                )

    @classmethod
    async def send_message(
        cls,
        bot,
        **kwargs,
    ):

        for tentativa in range(cls.MAX_TENTATIVAS):

            try:

                return await bot.send_message(
                    **kwargs,
                )

            except TimedOut:

                print(
                    f"[Telegram] Timeout "
                    f"(tentativa {tentativa + 1})"
                )

                if tentativa == cls.MAX_TENTATIVAS - 1:

                    raise

                await asyncio.sleep(
                    tentativa + 1
                )