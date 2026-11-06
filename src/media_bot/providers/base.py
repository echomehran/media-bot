"""Provider interface for legally downloadable media.

A *provider* adapts a single external source (Jamendo, Pixabay, the Internet
Archive, ...) into a common shape. Providers do not download files; they
return search results that carry the license under which each result may be
used. A separate downloader component decides whether to fetch a result based
on that license.

The interface deliberately encodes license information so that "is this legal
to redistribute?" is answered at the point of search, not deferred to the
downloader. A provider that cannot verify a result's license must not return
that result as downloadable.
"""

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


class MediaType(StrEnum):
    """The kinds of media a provider may return."""

    AUDIO = "audio"
    VIDEO = "video"


class License(StrEnum):
    """Licenses that permit redistribution through this bot.

    This enum is intentionally closed: adding a license is a deliberate code
    change, not a data value. There is no catch-all "other" member because an
    unrecognised license must be treated as non-downloadable. A provider that
    encounters a license not listed here should either map it to an existing
    member only when the mapping is genuinely accurate, or exclude the result.

    The values follow the naming used by Creative Commons and the relevant
    sources; they are not intended to be a legal taxonomy.
    """

    CC0 = "CC0"
    CC_BY = "CC-BY"
    CC_BY_SA = "CC-BY-SA"
    PUBLIC_DOMAIN = "public-domain"
    PIXABAY = "pixabay-license"


@dataclass(frozen=True)
class MediaResult:
    """A single search result from a provider.

    `download_url` is `None` for results whose license does not permit
    redistribution through the bot. Those results are still returned so that
    the user can be shown metadata, but the downloader must refuse to fetch
    them. `None` is a meaningful value here, not a missing one.
    """

    provider: str
    external_id: str
    title: str
    media_type: MediaType
    license: License
    license_url: str
    download_url: str | None


class MediaProvider(Protocol):
    """An adapter over a single source of legally downloadable media.

    Implementations must return only results whose license has been verified
    against the source at query time. Returning a result with an unknown
    license, or with `download_url` set for a license that does not permit
    redistribution, is a defect in the provider.
    """

    name: str

    async def search(
        self,
        query: str,
        media_type: MediaType | None = None,
    ) -> list[MediaResult]:
        """Return results for `query`, optionally restricted to one media type."""
        ...
