from typing import Final, cast

from redis.asyncio import Redis
from typing_extensions import override

from pix_erase.infrastructure.cache.cache_store import CacheStore


class RedisCacheStore(CacheStore):
    def __init__(self, redis_client: Redis) -> None:
        self._redis_client: Final[Redis] = redis_client

    @override
    async def set(
            self,
            name: str,
            value: bytes,
            ttl: int = 30
    ) -> None:
        await self._redis_client.set(name=name, value=value, ex=ttl)

    @override
    async def get(
            self,
            name: str,
    ) -> bytes:
        return cast(bytes, await self._redis_client.get(name=name))

    @override
    async def delete(self, name: str) -> None:
        await self._redis_client.delete(name)
