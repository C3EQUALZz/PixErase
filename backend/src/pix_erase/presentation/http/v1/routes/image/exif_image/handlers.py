from dataclasses import asdict
from inspect import getdoc
from typing import Final, Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status, Path

from pix_erase.application.common.views.image.read_image import ReadImageExifView
from pix_erase.application.queries.images.read_exif_from_image_by_id import (
    ReadExifFromImageByIDQueryHandler,
    ReadExifFromImageByIDQuery
)
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema, ExceptionSchemaRich
from pix_erase.presentation.http.v1.routes.image.exif_image.schemas import (
    ReadImageExifSchemaResponse,
    CameraSettingsSchemaResponse,
    ExposureSettingsSchemaResponse,
    FlashInfoSchemaResponse,
    GPSInfoSchemaResponse,
    DateTimeInfoSchemaResponse
)

exif_image_router: Final[APIRouter] = APIRouter(
    tags=["Image"],
    route_class=DishkaRoute,
)

ImageIDPathParameter = Path(
    title="The ID of the image that was upload",
    description="The ID of the image. We using UUID id's",
    examples=["19178bf6-8f84-406e-b213-102ec84fab9f", "75079971-fb0e-4e04-bf07-ceb57faebe84"],
)


@exif_image_router.get(
    "/id/{image_id}/exif/",
    status_code=status.HTTP_200_OK,
    summary="Get exif from image by id",
    description=getdoc(ReadExifFromImageByIDQueryHandler),
    response_model=ReadImageExifSchemaResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ExceptionSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ExceptionSchemaRich}
    }
)
async def read_exif_image_handler(
        image_id: Annotated[UUID, ImageIDPathParameter],
        interactor: FromDishka[ReadExifFromImageByIDQueryHandler]
) -> ReadImageExifSchemaResponse:
    query: ReadExifFromImageByIDQuery = ReadExifFromImageByIDQuery(
        image_id=image_id,
    )

    view: ReadImageExifView = await interactor(query)

    return ReadImageExifSchemaResponse(
        width=view.width,
        height=view.height,
        format=view.format,
        is_animated=view.is_animated,
        camera_settings=CameraSettingsSchemaResponse(**asdict(view.camera_settings)),
        exposure_settings=ExposureSettingsSchemaResponse(**asdict(view.exposure_settings)),
        flash_info=FlashInfoSchemaResponse(**asdict(view.flash_info)),
        gps_info=GPSInfoSchemaResponse(**asdict(view.gps_info)),
        datetime_info=DateTimeInfoSchemaResponse(**asdict(view.datetime_info)),
    )
