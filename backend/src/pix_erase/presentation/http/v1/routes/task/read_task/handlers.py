from inspect import getdoc

from fastapi import APIRouter, status, Path
from typing import Final, Annotated
from dishka.integrations.fastapi import DishkaRoute

from pix_erase.application.queries.tasks.read_task_by_id import ReadTaskByIDQueryHandler
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema, ExceptionSchemaRich

router: Final[APIRouter] = APIRouter(
    route_class=DishkaRoute,
    tags=["Task"]
)

TaskIDPath = Path(
    title="The ID of the task returned before",
    description="The ID of the image. We using UUID id's",
    examples=[
        "compress_image:19178bf6-8f84-406e-b213-102ec84fab9f",
        "resize_image:75079971-fb0e-4e04-bf07-ceb57faebe84"
    ],
)


@router.get(
    "/id/{task_id}/",
    status_code=status.HTTP_200_OK,
    summary="Reads task by id and gets info about it",
    description=getdoc(ReadTaskByIDQueryHandler),
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ExceptionSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ExceptionSchemaRich}
    }
)
async def read_task_by_id_handler(
        task_id: Annotated[str, TaskIDPath]
):
    ...
