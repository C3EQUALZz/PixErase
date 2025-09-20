from typing import Final, Iterable

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from pix_erase.presentation.http.v1.routes.auth.log_in.handlers import router as log_in_router
from pix_erase.presentation.http.v1.routes.auth.log_out.handlers import router as log_out_router
from pix_erase.presentation.http.v1.routes.auth.read_me.handlers import router as read_me_router
from pix_erase.presentation.http.v1.routes.auth.sign_up.handlers import router as sign_up_router

router: Final[APIRouter] = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    route_class=DishkaRoute,
)

sub_routers: Final[Iterable[APIRouter]] = (
    read_me_router,
    log_in_router,
    log_out_router,
    sign_up_router
)

for sub_router in sub_routers:
    router.include_router(sub_router)
