import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from media_bot.config.settings import DatabaseSettings

# Integration tests use a dedicated database configured through `.env.test`.
#
# `NullPool` is intentional here. pytest-asyncio creates a separate event
# loop for each test function, while asyncpg connections are tied to the
# event loop that created them. Reusing pooled connections across test
# loops can therefore cause:
#
#     got Future attached to a different loop
#
# Disabling connection pooling makes each test connection local to its
# current event loop. The application's production engine keeps normal
# pooling; this setting is specific to the test environment.
test_settings = DatabaseSettings(_env_file=".env.test")

test_engine = create_async_engine(
    test_settings.database_url,
    poolclass=NullPool,
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def dispose_test_engine():
    """Dispose the test engine after the entire integration test session.

    SQLAlchemy engines manage database resources even when `NullPool` is used.
    Explicitly disposing the engine makes the test suite's resource lifecycle
    clear and prevents connections from surviving beyond the pytest session.

    pytest automatically runs this fixture because of `autouse=True`.
    """
    yield

    await test_engine.dispose()


@pytest_asyncio.fixture
async def session() -> AsyncSession:
    """Provide an isolated database session for an integration test.

    The test gets a dedicated database connection and an outer transaction.
    `join_transaction_mode="create_savepoint"` allows application code to
    call `session.commit()` normally while SQLAlchemy keeps the test inside
    the outer transaction.

    At the end of the test, rolling back the outer transaction removes all
    changes made by that test, including changes that were committed through
    the session.

    This makes integration tests repeatable without manually deleting test
    data between runs.
    """
    async with test_engine.connect() as connection:
        transaction = await connection.begin()

        session = AsyncSession(
            bind=connection,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )

        try:
            yield session
        finally:
            await session.close()
            await transaction.rollback()
