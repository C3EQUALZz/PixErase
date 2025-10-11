from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from pix_erase.presentation.http.v1.routes.task.read_task.handlers import read_task_router
from typing import Final, Iterable

task_router: APIRouter = APIRouter(
    prefix="/task",
    route_class=DishkaRoute,
)

sub_routers: Final[Iterable[APIRouter]] = (
    read_task_router,
)

for sub_router in sub_routers:
    task_router.include_router(sub_router)