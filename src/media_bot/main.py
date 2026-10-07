import asyncio
import logging

from aiogram import Bot, Dispatcher

from media_bot.bot.router import router
from media_bot.config.settings import BotSettings


async def main() -> None:
    """Create the bot application and start long polling.

    BotSettings contains only configuration required by the Telegram bot.
    Keeping this dependency narrow means the bot does not need to know
    anything about database configuration at startup.
    """
    settings = BotSettings()

    bot = Bot(token=settings.bot_token)
    dispatcher = Dispatcher()

    dispatcher.include_router(router)

    logging.basicConfig(level=logging.INFO)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
