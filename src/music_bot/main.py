import asyncio
import logging

from aiogram import Bot, Dispatcher

from music_bot.bot.router import router
from music_bot.config.settings import Settings


async def main() -> None:
    settings = Settings()
    bot = Bot(token=settings.bot_token)
    dispatcher = Dispatcher()

    dispatcher.include_router(router)

    logging.basicConfig(level=logging.INFO)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())