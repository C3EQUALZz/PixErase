from dataclasses import asdict
from inspect import getdoc
from typing import Final, Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status, Security, Depends

from pix_erase.application.common.views.internet_protocol.ip_info import IPInfoView
from pix_erase.application.queries.internet_protocol.read_ip_info import ReadIPInfoQueryHandler, ReadIPInfoQuery
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema, ExceptionSchemaRich
from pix_erase.presentation.http.v1.common.fastapi_openapi_markers import cookie_scheme
from pix_erase.presentation.http.v1.routes.internet_protocol.read_ip_info.schemas import (
    ReadIPInfoSchemaRequest,
    ReadIPInfoSchemaResponse
)

read_ip_info_router: Final[APIRouter] = APIRouter(
    route_class=DishkaRoute,
    tags=["IP"]
)


@read_ip_info_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Read IP info",
    description=getdoc(ReadIPInfoQueryHandler),
    dependencies=[Security(cookie_scheme)],
    response_model=ReadIPInfoSchemaResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_408_REQUEST_TIMEOUT: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ExceptionSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ExceptionSchemaRich}
    }
)
async def read_ip_info_handler(
        request_schema: Annotated[ReadIPInfoSchemaRequest, Depends()],
        interactor: FromDishka[ReadIPInfoQueryHandler]
) -> ReadIPInfoSchemaResponse:
    query: ReadIPInfoQuery = ReadIPInfoQuery(
        ip_address=str(request_schema.destination_address),
    )

    view: IPInfoView = await interactor(query)

    return ReadIPInfoSchemaResponse(**asdict(view))
