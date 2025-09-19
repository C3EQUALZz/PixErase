from dataclasses import dataclass
from typing import final

from pix_erase.application.common.query_params.pagination import Pagination
from pix_erase.application.common.query_params.sorting import SortingOrder
from pix_erase.application.common.query_params.user_filters import UserQueryFilters
from pix_erase.application.common.views.user.read_user_by_id import ReadUserByIDView


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadAllUsersQuery:
    pagination: Pagination
    filters: UserQueryFilters
    sorting: SortingOrder


@final
class ReadAllUsersQueryHandler:
    def __init__(self) -> None: ...

    async def __call__(self, data: ReadAllUsersQuery) -> list[ReadUserByIDView]: ...
