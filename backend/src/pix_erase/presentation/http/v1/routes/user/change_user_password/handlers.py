from datetime import UTC, datetime
from inspect import getdoc
from typing import Annotated, Final
from uuid import UUID

from asgi_monitor.tracing import span
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path, Security
from opentelemetry import trace
from opentelemetry.trace import Tracer
from starlette import status

from pix_erase.application.commands.user.change_user_password import (
    ChangeUserPasswordCommand,
    ChangeUserPasswordCommandHandler,
)
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema, ExceptionSchemaRich
from pix_erase.presentation.http.v1.common.fastapi_openapi_markers import cookie_scheme
from pix_erase.presentation.http.v1.routes.user.change_user_password.schemas import ChangeUserPasswordRequestSchema

change_user_password_router: Final[APIRouter] = APIRouter(
    tags=["User"],
    route_class=DishkaRoute,
)
tracer: Final[Tracer] = trace.get_tracer(__name__)

UserIDPathParameter = Path(
    title="The ID of the user to get",
    description="The ID of the user to get. We using UUID id's",
    examples=["19178bf6-8f84-406e-b213-102ec84fab9f", "75079971-fb0e-4e04-bf07-ceb57faebe84"],
)


@change_user_password_router.patch(
    "/id/{user_id}/password",
    summary="Changes user password",
    description=getdoc(ChangeUserPasswordCommandHandler),
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(cookie_scheme)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ExceptionSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ExceptionSchemaRich},
    },
)
@span(
    tracer=tracer,
    name="span user change_password http",
    attributes={
        "http.request.method": "PATCH",
        "url.path": "/user/id/{user_id}/password",
        "http.route": "/user/id/{user_id}/password",
        "feature": "user",
        "action": "change_password",
        "time": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S"),
    },
)
async def change_user_password_handler(
    user_id: Annotated[UUID, UserIDPathParameter],
    request_schema: ChangeUserPasswordRequestSchema,
    interactor: FromDishka[ChangeUserPasswordCommandHandler],
) -> None:
    command: ChangeUserPasswordCommand = ChangeUserPasswordCommand(
        user_id=user_id,
        password=request_schema.password,
    )

    await interactor(command)
