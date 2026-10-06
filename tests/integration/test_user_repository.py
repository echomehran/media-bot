from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from music_bot.models.user import User
from music_bot.repositories.user import UserRepository


async def test_get_user_by_telegram_id(session: AsyncSession):
    user = User(
        telegram_id=123456789,
        username="test_user",
        first_name="Test",
        created_at=datetime.now(UTC),
    )

    session.add(user)
    await session.commit()

    repository = UserRepository(session)

    result = await repository.get_by_telegram_id(123456789)

    assert result is not None
    assert result.telegram_id == 123456789
    assert result.username == "test_user"
