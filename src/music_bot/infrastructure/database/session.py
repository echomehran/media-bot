from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from music_bot.config.settings import Settings

settings = Settings()

engine = create_async_engine(
    settings.database_url,
)

session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)