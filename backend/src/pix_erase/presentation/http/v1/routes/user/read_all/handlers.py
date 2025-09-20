from dataclasses import asdict
from inspect import getdoc
from typing import Final

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Security, status

from pix_erase.application.common.views.user.read_user_by_id import ReadUserByIDView
from pix_erase.application.queries.users.read_all import ReadAllUsersQueryHandler, ReadAllUsersQuery
from pix_erase.presentation.http.v1.common.fastapi_openapi_markers import cookie_scheme
from pix_erase.presentation.http.v1.routes.user.read_all.schemas import (
    ReadAllUsersRequestSchema,
    ReadAllUsersResponseSchema,
)
from pix_erase.presentation.http.v1.routes.user.read_by_id.schemas import ReadUserByIDResponse

router: Final[APIRouter] = APIRouter(
    prefix="/user",
    tags=["User"],
    route_class=DishkaRoute,
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    dependencies=[Security(cookie_scheme)],
    response_model=ReadAllUsersResponseSchema,
    summary="Get all users",
    description=getdoc(ReadAllUsersQueryHandler),
)
async def read_all_handler(
        request_schema: ReadAllUsersRequestSchema,
        interactor: FromDishka[ReadAllUsersQueryHandler],
) -> ReadAllUsersResponseSchema:
    query: ReadAllUsersQuery = ReadAllUsersQuery(
        limit=request_schema.pagination.limit,
        offset=request_schema.pagination.offset,
        sorting_field=request_schema.sorting_field,
        sorting_order=request_schema.sorting_order
    )

    view: list[ReadUserByIDView] = await interactor(query)

    return ReadAllUsersResponseSchema(
        users=[ReadUserByIDResponse(**asdict(user)) for user in view]
    )
