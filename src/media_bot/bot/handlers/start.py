from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    await message.answer(
        "Welcome to Media Bot! 🎵\n\n"
        "Send me a song name to search for music.\n\n"
        "Use /help to see available commands."
    )