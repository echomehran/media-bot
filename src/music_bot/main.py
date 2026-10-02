import asyncio

from aiogram import Bot, Dispatcher

from music_bot.config.settings import Settings


async def main() -> None:
    settings = Settings()
    bot = Bot(token=settings.bot_token)
    dispatcher = Dispatcher()

    print("Bot is running...")

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())