from inspect import getdoc
from typing import Final, Annotated
from datetime import datetime, UTC
from asgi_monitor.tracing import span
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path, Security
from opentelemetry import trace
from opentelemetry.trace import Tracer
from starlette import status

from pix_erase.application.commands.user.revoke_admin_by_id import (
    RevokeAdminByIDCommandHandler,
    RevokeAdminByIDCommand
)
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema, ExceptionSchemaRich
from pix_erase.presentation.http.v1.common.fastapi_openapi_markers import cookie_scheme

revoke_admin_router: Final[APIRouter] = APIRouter(
    tags=["User"],
    route_class=DishkaRoute,
)
tracer: Final[Tracer] = trace.get_tracer(__name__)

UserIDPathParameter = Path(
    title="The ID of the user to get",
    description="The ID of the user to get. We using UUID id's",
    examples=["19178bf6-8f84-406e-b213-102ec84fab9f", "75079971-fb0e-4e04-bf07-ceb57faebe84"],
)


@revoke_admin_router.patch(
    "/id/{id}/revoke-admin/",
    dependencies=[Security(cookie_scheme)],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Revoke Administrator access",
    description=getdoc(RevokeAdminByIDCommandHandler),
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ExceptionSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ExceptionSchemaRich}
    }
)
@span(
    tracer=tracer,
    name="span user revoke_admin http",
    attributes={
        "http.request.method": "PATCH",
        "url.path": "/user/id/{id}/revoke-admin/",
        "http.route": "/user/id/{id}/revoke-admin/",
        "feature": "user",
        "action": "revoke_admin",
        "time": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    }
)
async def revoke_admin_by_id_handler(
        user_id: Annotated[UUID, UserIDPathParameter],
        interactor: FromDishka[RevokeAdminByIDCommandHandler]
) -> None:
    command: RevokeAdminByIDCommand = RevokeAdminByIDCommand(
        user_id=user_id,
    )

    await interactor(command)
