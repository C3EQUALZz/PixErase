from inspect import getdoc
from typing import Final, Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status, UploadFile, File, Security

from pix_erase.application.commands.image.create_image import CreateImageCommandHandler, CreateImageCommand
from pix_erase.application.common.views.image.create_image import CreateImageView
from pix_erase.presentation.errors.image import BadFileFormatError
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema, ExceptionSchemaRich
from pix_erase.presentation.http.v1.common.fastapi_openapi_markers import cookie_scheme
from pix_erase.presentation.http.v1.routes.image.create_image.schemas import CreateImageSchemaResponse

create_image_router: Final[APIRouter] = APIRouter(
    route_class=DishkaRoute,
    tags=["Image"],
)


@create_image_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateImageSchemaResponse,
    summary="Handler for uploading image from user",
    description=getdoc(CreateImageCommandHandler),
    dependencies=[Security(cookie_scheme)],
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ExceptionSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ExceptionSchemaRich}
    }
)
async def create_image_handler(
        image: Annotated[UploadFile, File(description="A file for uploading to backend")],
        interactor: FromDishka[CreateImageCommandHandler]
) -> CreateImageSchemaResponse:
    if not image.content_type.startswith("image/"):
        msg = f"Invalid content type {image.content_type}"
        raise BadFileFormatError(msg)

    content: bytes = await image.read()
    filename: str = image.filename

    command: CreateImageCommand = CreateImageCommand(
        data=content,
        filename=filename,
    )

    view: CreateImageView = await interactor(command)

    return CreateImageSchemaResponse(image_id=view.image_id)
