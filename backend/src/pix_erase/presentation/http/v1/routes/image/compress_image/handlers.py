from inspect import getdoc
from typing import Final, Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status, Path

from pix_erase.application.commands.image.compress_image import CompressImageCommandHandler, CompressImageCommand
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema, ExceptionSchemaRich
from pix_erase.presentation.http.v1.routes.image.compress_image.schema import CompressImageRequestSchema

compress_image_router: Final[APIRouter] = APIRouter(
    route_class=DishkaRoute,
    tags=["Image"]
)

ImageIDPathParameter = Path(
    title="The ID of the image that was upload",
    description="The ID of the image. We using UUID id's",
    examples=["19178bf6-8f84-406e-b213-102ec84fab9f", "75079971-fb0e-4e04-bf07-ceb57faebe84"],
)


@compress_image_router.patch(
    "/id/{image_id}/compress/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Compress image",
    description=getdoc(CompressImageCommandHandler),
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ExceptionSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ExceptionSchemaRich}
    }
)
async def compress_image_handler(
        image_id: Annotated[UUID, ImageIDPathParameter],
        request_schema: CompressImageRequestSchema,
        interactor: FromDishka[CompressImageCommandHandler]
) -> None:
    command: CompressImageCommand = CompressImageCommand(
        image_id=image_id,
        quality=request_schema.quality
    )

    await interactor(command)
