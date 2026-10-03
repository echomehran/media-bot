import pytest

from music_bot.services.search import SearchService


@pytest.mark.asyncio
async def test_search_returns_query():
    service = SearchService()

    result = await service.search("Anthology Jim Reeves")

    assert result == "Searching for: Anthology Jim Reeves"