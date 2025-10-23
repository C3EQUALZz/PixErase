from typing import Final, Annotated
from inspect import getdoc
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status, Depends, Security

from pix_erase.application.commands.internet_protocol.ping_internet_protocol import (
    PingInternetProtocolCommandHandler,
    PingInternetProtocolCommand
)
from pix_erase.application.common.views.internet_protocol.ping_internet_protocol import PingInternetProtocolView
from pix_erase.presentation.http.v1.common.fastapi_openapi_markers import cookie_scheme
from pix_erase.presentation.http.v1.routes.internet_protocol.ping.schemas import PingSchemaRequest, PingSchemaResponse

ip_ping_router: Final[APIRouter] = APIRouter(
    route_class=DishkaRoute,
    tags=["IP"]
)


@ip_ping_router.get(
    "/ping/",
    status_code=status.HTTP_200_OK,
    summary="Ping service with known ip",
    response_model=PingSchemaResponse,
    description=getdoc(PingInternetProtocolCommandHandler),
    dependencies=[Security(cookie_scheme)],
)
async def ping_handler(
        request_schema: Annotated[PingSchemaRequest, Depends()],
        interactor: FromDishka[PingInternetProtocolCommandHandler]
) -> PingSchemaResponse:
    command: PingInternetProtocolCommand = PingInternetProtocolCommand(
        destination_address=str(request_schema.destination_address),
        timeout=request_schema.timeout,
        packet_size=request_schema.packet_size,
        ttl=request_schema.ttl,
    )

    view: PingInternetProtocolView = await interactor(command)

    return PingSchemaResponse(
        success=view.success,
        response_time_ms=view.response_time_ms,
        error_message=view.error_message,
        ttl=view.ttl,
        packet_size=view.packet_size,
    )
