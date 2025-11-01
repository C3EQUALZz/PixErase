from datetime import datetime, UTC
from typing import Final, Annotated

from asgi_monitor.tracing import span
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, status, Security
from opentelemetry import trace
from opentelemetry.trace import Tracer

from pix_erase.application.commands.internet_protocol.analyze_domain_info import (
    AnalyzeDomainQueryHandler,
    AnalyzeDomainQuery
)
from pix_erase.application.common.views.internet_protocol.analyze_domain import AnalyzeDomainView
from pix_erase.presentation.http.v1.common.exception_handler import ExceptionSchema, ExceptionSchemaRich
from pix_erase.presentation.http.v1.common.fastapi_openapi_markers import cookie_scheme
from pix_erase.presentation.http.v1.routes.internet_protocol.analyze_domain.schemas import (
    AnalyzeDomainResponse,
    AnalyzeDomainRequestSchema
)

analyze_domain_router: Final[APIRouter] = APIRouter(
    tags=["IP"],
    route_class=DishkaRoute,
)
tracer: Final[Tracer] = trace.get_tracer(__name__)


@analyze_domain_router.get(
    "/domain/",
    status_code=status.HTTP_200_OK,
    summary="Analyze domain info",
    response_model=AnalyzeDomainResponse,
    dependencies=[Security(cookie_scheme)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ExceptionSchemaRich},
    }
)
@span(
    tracer=tracer,
    name="span analyze domain http",
    attributes={
        "http.request.method": "GET",
        "url.path": "/ip/domain/",
        "http.route": "/ip/domain/",
        "feature": "domain",
        "action": "analyze",
        "time": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    }
)
async def analyze_domain(
        request_schema: Annotated[AnalyzeDomainRequestSchema, Depends()],
        interactor: FromDishka[AnalyzeDomainQueryHandler]
) -> AnalyzeDomainResponse:
    query: AnalyzeDomainQuery = AnalyzeDomainQuery(
        domain=request_schema.domain,
        timeout=request_schema.timeout
    )

    view: AnalyzeDomainView = await interactor(query)

    return AnalyzeDomainResponse(
        domain=view.domain_name,
        dns=view.dns_records,
        subdomains=view.subdomains,
        title=view.title,
    )
