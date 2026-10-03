from sqlalchemy import text

from music_bot.infrastructure.database.session import session_factory


async def test_database_connection():
    async with session_factory() as session:
        result = await session.execute(text("SELECT 1"))

        assert result.scalar_one() == 1