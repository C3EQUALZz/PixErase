from abc import abstractmethod
from typing import Protocol


class CertificateTransparencyPort(Protocol):
    @abstractmethod
    async def fetch_subdomains(self, domain: str, timeout: float) -> list[str]:
        ...
