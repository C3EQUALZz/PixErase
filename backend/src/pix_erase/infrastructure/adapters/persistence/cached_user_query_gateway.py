import json
import logging
from typing import Final, override

from pix_erase.application.common.ports.user.query_gateway import UserQueryGateway
from pix_erase.application.common.query_params.user_filters import UserListParams
from pix_erase.domain.user.entities.user import User
from pix_erase.domain.user.values.user_id import UserID
from pix_erase.infrastructure.cache.cache_store import CacheStore

logger: Final[logging.Logger] = logging.getLogger(__name__)


class CachedUserQueryGateway(UserQueryGateway):
    """
    Кэшированный декоратор для UserQueryGateway.

    Реализует паттерн декоратор для кэширования запросов пользователей.
    Сначала проверяет кэш, если данных нет - обращается к основному gateway.
    """

    USER_BY_ID_TTL: Final[int] = 300
    ALL_USERS_TTL: Final[int] = 60

    def __init__(self, user_query_gateway: UserQueryGateway, cache_store: CacheStore) -> None:
        self._user_query_gateway: Final[UserQueryGateway] = user_query_gateway
        self._cache_store: Final[CacheStore] = cache_store

    @staticmethod
    def _serialize_user(user: User) -> bytes:
        return json.dumps(user.serialize(), ensure_ascii=False).encode("utf-8")

    @staticmethod
    def _deserialize_user(data: bytes) -> User:
        return User.deserialize(json.loads(data.decode("utf-8")))

    def _serialize_users_list(self, users: list[User]) -> bytes:
        users_data: list[str] = [self._serialize_user(user).decode("utf-8") for user in users]
        return json.dumps(users_data, ensure_ascii=False).encode("utf-8")

    def _deserialize_users_list(self, data: bytes) -> list[User]:
        users_data = json.loads(data.decode("utf-8"))
        return [self._deserialize_user(user_data.encode("utf-8")) for user_data in users_data]

    @override
    async def read_user_by_id(self, user_id: UserID) -> User | None:
        cache_key: str = f"user:{user_id}"

        try:
            cached_data: bytes | None = await self._cache_store.get(cache_key)

            if cached_data is not None:
                logger.debug("User %s found in cache", user_id)
                return self._deserialize_user(cached_data)

            logger.debug("User %s not found in cache, querying database", user_id)

            user: User | None = await self._user_query_gateway.read_user_by_id(user_id)

            if user is not None:
                user_data = self._serialize_user(user)
                await self._cache_store.set(cache_key, user_data, self.USER_BY_ID_TTL)
                logger.debug("User %s cached for %d seconds", user_id, self.USER_BY_ID_TTL)

        except Exception:
            logger.exception("Error in cached read_user_by_id for user %s", user_id)
            return await self._user_query_gateway.read_user_by_id(user_id)
        else:
            return user

    @override
    async def read_all_users(self, user_list_params: UserListParams) -> list[User] | None:
        hash_for_key: int = hash(
            (
                user_list_params.pagination.limit,
                user_list_params.pagination.offset,
                user_list_params.sorting.sorting_field,
                user_list_params.sorting.sorting_order,
            )
        )

        cache_key: str = f"users:all:{abs(hash_for_key)}"

        try:
            cached_data: bytes | None = await self._cache_store.get(cache_key)

            if cached_data is not None:
                logger.debug("Users list found in cache for params: %s", user_list_params)
                return self._deserialize_users_list(cached_data)

            logger.debug("Users list not found in cache, querying database")

            users: list[User] | None = await self._user_query_gateway.read_all_users(user_list_params)

            if users is not None:
                users_data: bytes = self._serialize_users_list(users)
                await self._cache_store.set(cache_key, users_data, self.ALL_USERS_TTL)
                logger.debug("Users list cached for %d seconds", self.ALL_USERS_TTL)

        except Exception:
            logger.exception("Error in cached read_all_users")
            return await self._user_query_gateway.read_all_users(user_list_params)
        else:
            return users
