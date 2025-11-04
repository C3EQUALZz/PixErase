from datetime import UTC, datetime
from inspect import getdoc
from typing import Annotated, Final
from uuid import UUID

from asgi_monitor.tracing import span
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path, status
from opentelemetry import trace
from opentelemetry.trace import Tracer

from pix_erase.application.commands.image.delete_image import DeleteImageCommand, DeleteImageCommandHandler
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema, ExceptionSchemaRich

delete_image_router: Final[APIRouter] = APIRouter(route_class=DishkaRoute, tags=["Image"])
tracer: Final[Tracer] = trace.get_tracer(__name__)

ImageIDPathParameter = Path(
    title="The ID of the image that was upload",
    description="The ID of the image. We using UUID id's",
    examples=["19178bf6-8f84-406e-b213-102ec84fab9f", "75079971-fb0e-4e04-bf07-ceb57faebe84"],
)


@delete_image_router.delete(
    "/id/{image_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletes image from system. Only current user can delete his images",
    description=getdoc(DeleteImageCommandHandler),
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ExceptionSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ExceptionSchemaRich},
    },
)
@span(
    tracer=tracer,
    name="span image delete http",
    attributes={
        "http.request.method": "DELETE",
        "url.path": "/image/id/{image_id}/",
        "http.route": "/image/id/{image_id}/",
        "feature": "image",
        "action": "delete",
        "time": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S"),
    },
)
async def delete_image_handler(
    image_id: Annotated[UUID, ImageIDPathParameter], interactor: FromDishka[DeleteImageCommandHandler]
) -> None:
    command: DeleteImageCommand = DeleteImageCommand(
        image_id=image_id,
    )

    await interactor(command)
