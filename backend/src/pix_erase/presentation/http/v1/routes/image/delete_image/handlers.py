from inspect import getdoc
from typing import Final, Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status, Path

from pix_erase.application.commands.image.delete_image import DeleteImageCommandHandler, DeleteImageCommand

delete_image_router: Final[APIRouter] = APIRouter(
    route_class=DishkaRoute,
    tags=["Image"]
)

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

    }
)
async def delete_image_handler(
        image_id: Annotated[UUID, ImageIDPathParameter],
        interactor: FromDishka[DeleteImageCommandHandler]
) -> None:
    command: DeleteImageCommand = DeleteImageCommand(
        image_id=image_id,
    )

    await interactor(command)
