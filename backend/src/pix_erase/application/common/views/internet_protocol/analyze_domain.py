from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
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
    dns_records: Optional[dict[str, list[str]]] = None
    subdomains: list[str] = field(default_factory=list)
    title: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
