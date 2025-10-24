from typing import Protocol
from abc import abstractmethod


class CacheStore(Protocol):
    @abstractmethod
    async def set(
            self,
            name: str,
            value: bytes,
            ttl: int
    ) -> None:
        ...

    @abstractmethod
    async def get(
            self,
            name: str,
    ) -> bytes | None:
        ...

    @abstractmethod
    async def delete(
            self,
            name: str
    ) -> None:
        ...
