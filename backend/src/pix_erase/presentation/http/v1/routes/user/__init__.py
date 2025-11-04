from collections.abc import Iterable
from typing import Final

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from pix_erase.presentation.http.v1.routes.user.activate_user.handlers import activate_user_router
from pix_erase.presentation.http.v1.routes.user.change_user_email.handlers import change_user_email_router
from pix_erase.presentation.http.v1.routes.user.change_user_name.handlers import change_user_name_router
from pix_erase.presentation.http.v1.routes.user.change_user_password.handlers import change_user_password_router
from pix_erase.presentation.http.v1.routes.user.create.handlers import create_user_router
from pix_erase.presentation.http.v1.routes.user.delete.handlers import delete_router
from pix_erase.presentation.http.v1.routes.user.grant_admin.handlers import grant_admin_router
from pix_erase.presentation.http.v1.routes.user.read.handlers import read_router
from pix_erase.presentation.http.v1.routes.user.read_all.handlers import read_all_router
from pix_erase.presentation.http.v1.routes.user.revoke_admin.handlers import revoke_admin_router

user_router: Final[APIRouter] = APIRouter(
    prefix="/user",
    tags=["User"],
    route_class=DishkaRoute,
)

sub_routers: Final[Iterable[APIRouter]] = (
    create_user_router,
    revoke_admin_router,
    change_user_email_router,
    change_user_name_router,
    change_user_password_router,
    delete_router,
    activate_user_router,
    read_router,
    read_all_router,
    grant_admin_router,
)

for sub_router in sub_routers:
    user_router.include_router(sub_router)
