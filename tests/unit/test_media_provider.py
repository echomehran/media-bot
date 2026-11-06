"""Tests for the MediaProvider protocol and its result types.

These tests exist to keep the interface's shape stable. Any change to
`MediaProvider.search` or to the fields of `MediaResult` will fail here,
which is the intended moment to reconsider the interface rather than to
adapt it quietly to a single provider's needs.
"""

from media_bot.providers.base import (
    License,
    MediaProvider,
    MediaResult,
    MediaType,
)


class FakeProvider:
    """A minimal in-memory provider used to exercise the protocol."""

    name = "fake"

    async def search(
        self,
        query: str,
        media_type: MediaType | None = None,
    ) -> list[MediaResult]:
        results = [
            MediaResult(
                provider="fake",
                external_id="1",
                title=f"Audio result for {query}",
                media_type=MediaType.AUDIO,
                license=License.CC_BY,
                license_url="https://example.test/license/cc-by",
                download_url="https://example.test/1.mp3",
            ),
            MediaResult(
                provider="fake",
                external_id="2",
                title=f"Video result for {query}",
                media_type=MediaType.VIDEO,
                license=License.CC_BY,
                license_url="https://example.test/license/cc-by",
                download_url=None,
            ),
        ]
        if media_type is not None:
            results = [r for r in results if r.media_type is media_type]
        return results


async def test_provider_protocol_is_usable():
    """A class satisfying the protocol can be used through it.

    This is the core stability check: the fake provider is typed as
    `MediaProvider`, so `await provider.search(...)` type-checks and runs.
    """
    provider: MediaProvider = FakeProvider()

    results = await provider.search("test")

    assert len(results) == 2
    assert results[0].license is License.CC_BY
    assert results[0].media_type is MediaType.AUDIO


async def test_search_can_filter_by_media_type():
    """The optional `media_type` filter narrows results."""
    provider: MediaProvider = FakeProvider()

    results = await provider.search("test", media_type=MediaType.VIDEO)

    assert len(results) == 1
    assert results[0].media_type is MediaType.VIDEO


def test_media_result_allows_metadata_only_results():
    """A result may have no `download_url`, representing search-only content.

    This is how providers advertise results whose license does not permit
    redistribution through the bot. The downloader must check
    `download_url is not None` before attempting a fetch. `None` is a
    meaningful value, not a missing one.
    """
    result = MediaResult(
        provider="fake",
        external_id="2",
        title="Metadata only",
        media_type=MediaType.VIDEO,
        license=License.CC_BY,
        license_url="https://example.test/license/cc-by",
        download_url=None,
    )

    assert result.download_url is None


def test_media_result_is_immutable():
    """Mutating a result's license is not allowed.

    Results are value objects. If a caller needs a different result, it must
    construct a new one; that keeps the license attached to the data it
    describes rather than to a mutable field.
    """
    result = MediaResult(
        provider="fake",
        external_id="3",
        title="Immutable",
        media_type=MediaType.AUDIO,
        license=License.CC0,
        license_url="https://example.test/license/cc0",
        download_url="https://example.test/3.mp3",
    )

    try:
        result.license = License.CC_BY  # type: ignore[misc]
    except Exception:  # noqa: BLE001 - any exception is acceptable here
        # `dataclasses.FrozenInstanceError` on CPython; asserting on the
        # specific type would couple this test to CPython's exception.
        assert True
    else:
        raise AssertionError("MediaResult should be immutable")
