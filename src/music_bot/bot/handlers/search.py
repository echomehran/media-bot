from aiogram import Router
from aiogram.types import Message

from music_bot.services.search import SearchService

router = Router()
search_service = SearchService()


@router.message()
async def search_handler(message: Message) -> None:
    query = message.text

    if not query:
        return

    result = await search_service.search(query)

    await message.answer(result)