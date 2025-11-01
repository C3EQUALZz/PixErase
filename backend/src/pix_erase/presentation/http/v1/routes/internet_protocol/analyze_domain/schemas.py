from pydantic import BaseModel, Field, StringConstraints, IPvAnyAddress
from typing import Annotated

DomainName = Annotated[
    str,
    StringConstraints(pattern=r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$")
]


class AnalyzeDomainRequestSchema(BaseModel):
    domain: IPvAnyAddress | DomainName = Field(
        ...,
        description="Target domain to processing",
        examples=["https://www.example.com"]
    )
    timeout: float = Field(
        ...,
        description="Timeout in seconds",
        ge=0.1,
        examples=[0.1, 0.2, 1.2]
    )


class AnalyzeDomainResponse(BaseModel):
    domain: IPvAnyAddress | DomainName = Field(
        ...,
        description="Target domain to processing",
        examples=["https://www.example.com", "www.example.com"]
    )
    dns: dict[str, list[str]] | None
    subdomains: list[IPvAnyAddress | DomainName] = Field(
        ...,
        description="Subdomains for this domain",
        examples=["www.example1.com", "www.example2.com"]
    )
    title: str = Field(

    )
