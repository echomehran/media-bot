from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message"
    )