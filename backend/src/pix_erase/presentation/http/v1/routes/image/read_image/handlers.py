from inspect import getdoc
from typing import Final, Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status, Path
from starlette.responses import StreamingResponse

from pix_erase.application.common.views.image.read_image import ReadImageByIDView
from pix_erase.application.queries.images.read_by_id import ReadImageByIDQueryHandler, ReadImageByIDQuery
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema, ExceptionSchemaRich

read_image_router: Final[APIRouter] = APIRouter(
    route_class=DishkaRoute,
    tags=["Image"],
)

ImageIDPathParameter = Path(
    title="The ID of the image that was upload",
    description="The ID of the image. We using UUID id's",
    examples=["19178bf6-8f84-406e-b213-102ec84fab9f", "75079971-fb0e-4e04-bf07-ceb57faebe84"],
)


@read_image_router.get(
    "/id/{image_id}/",
    status_code=status.HTTP_200_OK,
    response_class=StreamingResponse,
    summary="Streaming image by image id",
    description=getdoc(ReadImageByIDQueryHandler),
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ExceptionSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ExceptionSchemaRich}
    }
)
async def read_image_by_id_handler(
        image_id: Annotated[UUID, ImageIDPathParameter],
        interactor: FromDishka[ReadImageByIDQueryHandler]
) -> StreamingResponse:
    query: ReadImageByIDQuery = ReadImageByIDQuery(
        image_id=image_id,
    )

    view: ReadImageByIDView = await interactor(query)

    return StreamingResponse(
        content=view.data,
        media_type=view.content_type,
        headers={
            "Content-Length": str(view.content_length),
            "Content-Disposition": f"inline; filename=\"{view.name}\"",
            "Last-Modified": view.updated_at.strftime("%a, %d %b %Y %H:%M:%S GMT"),
            "ETag": view.etag or "",
            "Cache-Control": "public, max-age=3600"
        }
    )
