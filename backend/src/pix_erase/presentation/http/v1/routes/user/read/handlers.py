from inspect import getdoc
from typing import TYPE_CHECKING, Annotated, Final
from datetime import datetime, UTC
from asgi_monitor.tracing import span
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path, Security, status
from opentelemetry import trace
from opentelemetry.trace import Tracer

from pix_erase.application.queries.users.read_by_id import ReadUserByIDQuery, ReadUserByIDQueryHandler
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema, ExceptionSchemaRich
from pix_erase.presentation.http.v1.common.fastapi_openapi_markers import cookie_scheme
from pix_erase.presentation.http.v1.routes.user.read.schemas import ReadUserByIDResponse

if TYPE_CHECKING:
    from pix_erase.application.common.views.user.read_user_by_id import ReadUserByIDView

read_router: Final[APIRouter] = APIRouter(
    tags=["User"],
    route_class=DishkaRoute,
)
tracer: Final[Tracer] = trace.get_tracer(__name__)

UserIDPathParameter = Path(
    title="The ID of the user to get",
    description="The ID of the user to get. We using UUID id's",
    examples=["19178bf6-8f84-406e-b213-102ec84fab9f", "75079971-fb0e-4e04-bf07-ceb57faebe84"],
)


@read_router.get(
    "/id/{user_id}/",
    status_code=status.HTTP_200_OK,
    dependencies=[Security(cookie_scheme)],
    response_model=ReadUserByIDResponse,
    summary="Get user by id",
    description=getdoc(ReadUserByIDQueryHandler),
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
    name="span user read_by_id http",
    attributes={
        "http.request.method": "GET",
        "url.path": "/user/id/{user_id}/",
        "http.route": "/user/id/{user_id}/",
        "feature": "user",
        "action": "read_by_id",
        "time": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    }
)
async def read_user_by_id_handler(
        user_id: Annotated[UUID, UserIDPathParameter], interactor: FromDishka[ReadUserByIDQueryHandler]
) -> ReadUserByIDResponse:
    query: ReadUserByIDQuery = ReadUserByIDQuery(
        user_id=user_id,
    )

    view: ReadUserByIDView = await interactor(data=query)

    return ReadUserByIDResponse(
        id=view.user_id,
        email=view.email,  # type: ignore[arg-type, unused-ignore]
        name=view.name,
        role=view.role,  # type: ignore[arg-type, unused-ignore]
    )
