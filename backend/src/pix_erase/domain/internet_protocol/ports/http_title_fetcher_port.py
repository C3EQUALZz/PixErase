from abc import abstractmethod
from typing import Protocol


class HttpTitleFetcherPort(Protocol):
    @abstractmethod
    async def fetch_title(self, host: str) -> str:
        ...
