import logging
import re
from typing import Final, override

from pix_erase.domain.internet_protocol.ports.http_title_fetcher_port import HttpTitleFetcherPort
from pix_erase.infrastructure.errors.http import HttpError
from pix_erase.infrastructure.http.base import HttpClient, HttpResponse

logger: Final[logging.Logger] = logging.getLogger(__name__)
_TITLE_RE: Final[re.Pattern[str]] = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


class HttpTitleFetcher(HttpTitleFetcherPort):
    def __init__(self, http_client: HttpClient) -> None:
        self._http: Final[HttpClient] = http_client

    @override
    async def fetch_title(self, host: str) -> str:
        logger.debug("Started fetching title for %s", host)
        for scheme in ("https", "http"):
            logger.debug("Trying scheme %s for host: %s", scheme, host)
            url: str = f"{scheme}://{host}"
            try:
                resp: HttpResponse = await self._http.get(url, timeout=5.0)
                html: str = resp.text()
                match: re.Match[str] | None = _TITLE_RE.search(html)
                if match:
                    return match.group(1).strip()[:256]
            except HttpError:
                logger.exception("Failed to fetch title for %s", host)
                continue
        return "N/A"
