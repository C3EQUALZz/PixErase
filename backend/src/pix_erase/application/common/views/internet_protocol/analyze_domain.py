from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class AnalyzeDomainView:
    """
    View for domain analysis response.

    This view represents the domain analysis data
    that will be returned to the client.
    """

    domain_id: UUID
    domain_name: str
    dns_records: dict[str, list[str]] | None = None
    subdomains: list[str] = field(default_factory=list)
    title: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
