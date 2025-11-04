from abc import abstractmethod
from typing import Protocol


class CacheStore(Protocol):
    @abstractmethod
    async def set(self, name: str, value: bytes, ttl: int) -> None: ...

    @abstractmethod
    async def get(
        self,
        name: str,
    ) -> bytes | None: ...

    @abstractmethod
    async def delete(self, name: str) -> None: ...
