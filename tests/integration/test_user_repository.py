from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from media_bot.models.user import User
from media_bot.repositories.user import UserRepository


async def test_get_user_by_telegram_id(session: AsyncSession):
    """Return the persisted user whose telegram_id matches the query."""
    user = User(
        telegram_id=100000001,
        username="test_user",
        first_name="Test",
        created_at=datetime.now(UTC),
    )
    session.add(user)
    await session.commit()

    repository = UserRepository(session)
    result = await repository.get_by_telegram_id(100000001)

    # The repository must return a row at all.
    assert result is not None
    # Every persisted, application-visible field must round-trip correctly.
    # `id` is assigned by the database, so this also proves the insert worked.
    assert result.id is not None
    assert result.telegram_id == 100000001
    assert result.username == "test_user"
    assert result.first_name == "Test"
    # `created_at` must come back timezone-aware (the behavior introduced by
    # migration 974af911e416), and the value must survive the DB round-trip.
    # We allow sub-second drift because PostgreSQL stores microsecond precision
    # and we do not want the test to depend on the DB clock matching Python's.
    assert result.created_at.tzinfo is not None
    assert abs((result.created_at - user.created_at).total_seconds()) < 1


async def test_get_user_by_telegram_id_returns_none_for_unknown_id(
    session: AsyncSession,
):
    """Return None when no user has the requested telegram_id.

    A different user is inserted first so that this test also proves the
    repository filters by `telegram_id` rather than merely returning
    "a user" when the table is non-empty.
    """
    session.add(
        User(
            telegram_id=100000002,
            username="other_user",
            first_name="Other",
            created_at=datetime.now(UTC),
        )
    )
    await session.commit()

    repository = UserRepository(session)
    result = await repository.get_by_telegram_id(999999999)

    assert result is None


async def test_get_user_by_telegram_id_returns_the_matching_user(
    session: AsyncSession,
):
    """Return the user with the requested telegram_id, not merely any user.

    Two users are inserted so that the test distinguishes "the repository
    filtered by telegram_id" from "the repository returned some row." With
    only one row present, those two behaviours are indistinguishable.
    """
    session.add_all(
        [
            User(
                telegram_id=100000003,
                username="first",
                first_name="First",
                created_at=datetime.now(UTC),
            ),
            User(
                telegram_id=100000004,
                username="second",
                first_name="Second",
                created_at=datetime.now(UTC),
            ),
        ]
    )
    await session.commit()

    repository = UserRepository(session)
    result = await repository.get_by_telegram_id(100000004)

    assert result is not None
    assert result.telegram_id == 100000004
    assert result.username == "second"
    assert result.first_name == "Second"
