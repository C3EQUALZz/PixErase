from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from pix_erase.application.common.query_params.pagination import Pagination
from pix_erase.application.common.query_params.sorting import SortingOrder
from pix_erase.application.common.query_params.user_filters import UserQueryFilters
from pix_erase.presentation.http.v1.routes.user.read.schemas import ReadUserByIDResponse


class PaginationSchema(BaseModel):
    model_config = ConfigDict(frozen=True)

    limit: int = Field(default=20, ge=1, description="Limit for pagination", title="Pagination", validate_default=True)
    offset: int = Field(
        default=0, ge=0, le=100, description="Offset for pagination", title="Pagination", validate_default=True
    )


class ReadAllUsersRequestSchema(BaseModel):
    model_config = ConfigDict(frozen=True)

    pagination: Annotated[Pagination, PaginationSchema]
    sorting_field: Annotated[
        UserQueryFilters,
        Field(
            default=UserQueryFilters.email,
            description="Field for sorting",
            title="User sorting field",
            examples=["email", "name"],
            validate_default=True,
        ),
    ]
    sorting_order: Annotated[
        SortingOrder,
        Field(
            description="Order for sorting",
            examples=["ASC", "DESC"],
            title="Pagination",
            validate_default=True,
        ),
    ] = SortingOrder.DESC


class ReadAllUsersResponseSchema(BaseModel):
    model_config = ConfigDict(frozen=True)

    users: list[ReadUserByIDResponse] = Field(
        default=[],
        description="List of users",
        title="Users",
    )
