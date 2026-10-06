from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def test_database_connection(session: AsyncSession):
    """Verify that the integration-test database accepts SQL queries.

    `SELECT 1` is a minimal database connectivity check. It does not test
    application behavior; it only proves that the test session can establish
    a working PostgreSQL connection and execute a query.
    """
    result = await session.execute(text("SELECT 1"))

    assert result.scalar_one() == 1
