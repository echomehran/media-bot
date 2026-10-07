from aiogram import Router

from media_bot.bot.handlers.help import router as help_router
from media_bot.bot.handlers.search import router as search_router
from media_bot.bot.handlers.start import router as start_router

router = Router()

router.include_router(start_router)
router.include_router(help_router)
router.include_router(search_router)