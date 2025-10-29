from inspect import getdoc
from typing import Final, Annotated
from datetime import datetime, UTC
from asgi_monitor.tracing import span
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status, Path
from opentelemetry import trace
from opentelemetry.trace import Tracer

from pix_erase.application.commands.image.rotate_image import RotateImageCommandHandler, RotateImageCommand
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema, ExceptionSchemaRich
from pix_erase.presentation.http.v1.routes.image.rotate_image.schemas import (
    RotateImageSchemaRequest,
    RotateImageSchemaResponse
)

rotate_image_router: Final[APIRouter] = APIRouter(
    route_class=DishkaRoute,
    tags=["Image"]
)
tracer: Final[Tracer] = trace.get_tracer(__name__)

ImageIDPathParameter = Path(
    title="The ID of the image that was upload",
    description="The ID of the image. We using UUID id's",
    examples=["19178bf6-8f84-406e-b213-102ec84fab9f", "75079971-fb0e-4e04-bf07-ceb57faebe84"],
)


@rotate_image_router.patch(
    "/id/{image_id}/rotate/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Rotates image that user uploaded in system",
    description=getdoc(RotateImageCommandHandler),
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ExceptionSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ExceptionSchemaRich}
    },
    response_model=RotateImageSchemaResponse
)
@span(
    tracer=tracer,
    name="span image rotate http",
    attributes={
        "http.request.method": "PATCH",
        "url.path": "/image/id/{image_id}/rotate/",
        "http.route": "/image/id/{image_id}/rotate/",
        "feature": "image",
        "action": "rotate",
        "time": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    }
)
async def rotate_image_handler(
        image_id: Annotated[UUID, ImageIDPathParameter],
        request_schema: RotateImageSchemaRequest,
        interactor: FromDishka[RotateImageCommandHandler],
) -> RotateImageSchemaResponse:
    command: RotateImageCommand = RotateImageCommand(
        image_id=image_id,
        angle=request_schema.angle,
    )

    task_id: str = await interactor(command)

    return RotateImageSchemaResponse(task_id=task_id)
