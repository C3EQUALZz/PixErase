from datetime import UTC, datetime
from uuid import uuid4
from unittest.mock import AsyncMock

import pytest

from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.views.internet_protocol.analyze_domain import AnalyzeDomainView
from pix_erase.application.queries.internet_protocol.analyze_domain_info import (
    AnalyzeDomainQuery,
    AnalyzeDomainQueryHandler,
)
from pix_erase.domain.internet_protocol.entities.internet_domain import InternetDomain
from pix_erase.domain.internet_protocol.services.internet_domain_service import InternetDomainService
from pix_erase.domain.internet_protocol.values import DnsRecords, DomainName
from pix_erase.domain.internet_protocol.values.domain_id import DomainID


@pytest.mark.asyncio
async def test_analyze_domain_success(
    fake_current_user_service: CurrentUserService,
    fake_internet_domain_service: InternetDomainService,
) -> None:
    # Arrange
    domain_id: DomainID = DomainID(uuid4())
    now = datetime.now(UTC)
    internet_domain = InternetDomain(
        id=domain_id,
        domain_name=DomainName("example.com"),
        dns_records=DnsRecords(a=["1.1.1.1"], aaaa=[], mx=[], ns=[], txt=[], cname=[], soa=[]),
        subdomains=[DomainName("api.example.com")],
        title="Example",
        created_at=now,
        updated_at=now,
    )
    fake_internet_domain_service.analyze_domain = AsyncMock(return_value=internet_domain)

    sut = AnalyzeDomainQueryHandler(
        current_user_service=fake_current_user_service,
        internet_domain_service=fake_internet_domain_service,
    )

    query = AnalyzeDomainQuery(domain="example.com", timeout=5)

    # Act
    view: AnalyzeDomainView = await sut(query)

    # Assert
    assert view.domain_id == domain_id
    assert view.domain_name == "example.com"
    assert view.dns_records is not None and "A" in view.dns_records
    assert view.subdomains == ["api.example.com"]
    assert view.title == "Example"
    assert view.created_at == now and view.updated_at == now

