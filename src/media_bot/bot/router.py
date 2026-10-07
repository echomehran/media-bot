from aiogram import Router

from music_bot.bot.handlers.help import router as help_router
from music_bot.bot.handlers.search import router as search_router
from music_bot.bot.handlers.start import router as start_router

router = Router()

router.include_router(start_router)
router.include_router(help_router)
router.include_router(search_router)