from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from music_bot.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        statement = select(User).where(User.telegram_id == telegram_id)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()
