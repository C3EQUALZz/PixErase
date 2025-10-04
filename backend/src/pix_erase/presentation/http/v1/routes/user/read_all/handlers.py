from dataclasses import asdict
from inspect import getdoc
from typing import Final, Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Security, status, Depends

from pix_erase.application.common.views.user.read_user_by_id import ReadUserByIDView
from pix_erase.application.queries.users.read_all import ReadAllUsersQueryHandler, ReadAllUsersQuery
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema, ExceptionSchemaRich
from pix_erase.presentation.http.v1.common.fastapi_openapi_markers import cookie_scheme
from pix_erase.presentation.http.v1.routes.user.read_all.schemas import (
    ReadAllUsersRequestSchema,
    ReadAllUsersResponseSchema,
)
from pix_erase.presentation.http.v1.routes.user.read.schemas import ReadUserByIDResponse

read_all_router: Final[APIRouter] = APIRouter(
    tags=["User"],
    route_class=DishkaRoute,
)


@read_all_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    dependencies=[Security(cookie_scheme)],
    response_model=ReadAllUsersResponseSchema,
    summary="Get all users",
    description=getdoc(ReadAllUsersQueryHandler),
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ExceptionSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ExceptionSchemaRich}
    }
)
async def read_all_handler(
        request_schema: Annotated[ReadAllUsersRequestSchema, Depends()],
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
