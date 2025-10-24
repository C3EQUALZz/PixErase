from typing import Final, Iterable

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from pix_erase.presentation.http.v1.routes.internet_protocol.ping.handlers import ip_ping_router
from pix_erase.presentation.http.v1.routes.internet_protocol.read_ip_info.handlers import read_ip_info_router
from pix_erase.presentation.http.v1.routes.internet_protocol.scan_ports.handlers import router as scan_ports_router

ip_router: Final[APIRouter] = APIRouter(
    prefix="/ip",
    route_class=DishkaRoute,
    tags=["IP"]
)

sub_routers: Final[Iterable[APIRouter]] = (
    ip_ping_router,
    read_ip_info_router,
    scan_ports_router,
)

for sub_router in sub_routers:
    ip_router.include_router(sub_router)
