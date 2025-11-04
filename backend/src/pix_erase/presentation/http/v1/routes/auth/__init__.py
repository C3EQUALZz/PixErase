from collections.abc import Iterable
from typing import Final

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from pix_erase.presentation.http.v1.routes.auth.log_in.handlers import log_in_router
from pix_erase.presentation.http.v1.routes.auth.log_out.handlers import log_out_router
from pix_erase.presentation.http.v1.routes.auth.read_me.handlers import read_me_router
from pix_erase.presentation.http.v1.routes.auth.sign_up.handlers import sign_up_router

auth_router: Final[APIRouter] = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    route_class=DishkaRoute,
)

sub_routers: Final[Iterable[APIRouter]] = (read_me_router, log_in_router, log_out_router, sign_up_router)

for sub_router in sub_routers:
    auth_router.include_router(sub_router)
