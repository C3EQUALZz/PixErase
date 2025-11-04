from datetime import UTC, datetime
from inspect import getdoc
from typing import Annotated, Final
from uuid import UUID

from asgi_monitor.tracing import span
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path, Security, status
from opentelemetry import trace
from opentelemetry.trace import Tracer

from pix_erase.application.commands.user.delete_user_by_id import DeleteUserByIDCommand, DeleteUserByIDCommandHandler
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema, ExceptionSchemaRich
from pix_erase.presentation.http.v1.common.fastapi_openapi_markers import cookie_scheme

delete_router: Final[APIRouter] = APIRouter(
    route_class=DishkaRoute,
    tags=["User"],
)
tracer: Final[Tracer] = trace.get_tracer(__name__)

UserIDPathParameter = Path(
    title="The ID of the user to get",
    description="The ID of the user to get. We using UUID id's",
    examples=["19178bf6-8f84-406e-b213-102ec84fab9f", "75079971-fb0e-4e04-bf07-ceb57faebe84"],
)


@delete_router.delete(
    "/id/{user_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletes user by id",
    description=getdoc(DeleteUserByIDCommandHandler),
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
    name="span user delete http",
    attributes={
        "http.request.method": "DELETE",
        "url.path": "/user/id/{user_id}/",
        "http.route": "/user/id/{user_id}/",
        "feature": "user",
        "action": "delete_by_id",
        "time": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S"),
    },
)
async def delete_user_by_id_handler(
    user_id: Annotated[UUID, UserIDPathParameter], interactor: FromDishka[DeleteUserByIDCommandHandler]
) -> None:
    command: DeleteUserByIDCommand = DeleteUserByIDCommand(user_id=user_id)

    await interactor(command)
