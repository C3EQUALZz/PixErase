import logging
from typing import Any, Final, override

from pix_erase.domain.internet_protocol.ports.certificate_transparency_port import CertificateTransparencyPort
from pix_erase.infrastructure.errors.http import HttpError
from pix_erase.infrastructure.http.base import HttpClient, HttpResponse

logger: Final[logging.Logger] = logging.getLogger(__name__)


class CrtShCertificateTransparencyPort(CertificateTransparencyPort):
    _BASE_URL: Final[str] = "https://crt.sh/?q=%25.{domain}&output=json"

    def __init__(self, http_client: HttpClient) -> None:
        self._http: Final[HttpClient] = http_client

    @override
    async def fetch_subdomains(self, domain: str, timeout: float) -> list[str]:
        logger.debug(
            "Started fetching subdomains for domain: %s with timeout: %s",
            domain,
            timeout,
        )

        url: str = self._BASE_URL.format(domain=domain)

        logger.debug("Format url for search: %s", url)

        try:
            logger.debug("Fetching subdomains for domain: %s", domain)
            resp: HttpResponse = await self._http.get(url, timeout=timeout)
            logger.debug("Got response: %s", resp)

            if resp.status_code != 200:
                logger.warning("Got response with status code: %s for CrtSh", resp.status_code)
                return []

            rows: list[dict[str, Any]] = resp.json()

            logger.debug("Got all rows: %s from json", rows)

            names: set[str] = set()

            for row in rows:
                value = row.get("name_value")

                if not value:
                    continue

                names |= {name.strip().lower() for name in str(value).split() if name.endswith(domain)}

            return sorted(names)

        except HttpError:
            logger.exception("Error was occurred while fetching url: %s", url)
            return []
