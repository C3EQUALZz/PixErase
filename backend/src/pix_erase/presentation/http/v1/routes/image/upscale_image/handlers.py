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

from pix_erase.application.commands.image.upscale_image import UpscaleImageCommandHandler, UpscaleImageCommand
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema, ExceptionSchemaRich
from pix_erase.presentation.http.v1.routes.image.upscale_image.schemas import (
    UpscaleImageRequestSchema,
    UpscaleImageSchemeResponse
)

upscale_image_router: Final[APIRouter] = APIRouter(
    route_class=DishkaRoute,
    tags=["Image"]
)
tracer: Final[Tracer] = trace.get_tracer(__name__)

ImageIDPathParameter = Path(
    title="The ID of the image that was upload",
    description="The ID of the image. We using UUID id's",
    examples=["19178bf6-8f84-406e-b213-102ec84fab9f", "75079971-fb0e-4e04-bf07-ceb57faebe84"],
)


@upscale_image_router.patch(
    "/id/{image_id}/upscale/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Upscale an image using ai at several times",
    description=getdoc(UpscaleImageCommandHandler),
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ExceptionSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ExceptionSchemaRich}
    },
    response_model=UpscaleImageSchemeResponse
)
@span(
    tracer=tracer,
    name="span image upscale http",
    attributes={
        "http.request.method": "PATCH",
        "url.path": "/image/id/{image_id}/upscale/",
        "http.route": "/image/id/{image_id}/upscale/",
        "feature": "image",
        "action": "upscale",
        "time": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    }
)
async def upscale_image_handler(
        image_id: Annotated[UUID, ImageIDPathParameter],
        schema_request: UpscaleImageRequestSchema,
        interactor: FromDishka[UpscaleImageCommandHandler]
) -> UpscaleImageSchemeResponse:
    command: UpscaleImageCommand = UpscaleImageCommand(
        image_id=image_id,
        algorithm=schema_request.algorithm,
        scale=schema_request.scale,
    )

    task_id: str = await interactor(command)

    return UpscaleImageSchemeResponse(task_id=task_id)
