from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def search_handler(message: Message) -> None:
    query = message.text

    if not query:
        return

    await message.answer(f"Searching for: {query}")