from dataclasses import dataclass
from typing import TypedDict


class DnsRecordsDict(TypedDict):
    A: list[str]
    AAAA: list[str]
    CNAME: list[str]
    MX: list[str]
    NS: list[str]
    SOA: list[str]
    TXT: list[str]


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class DnsRecords:
    """
    Value object representing DNS records for a domain.

    Contains different types of DNS records including A, AAAA, MX, NS, TXT, CNAME, and SOA.
    """

    a: list[str]
    aaaa: list[str]
    mx: list[str]
    ns: list[str]
    txt: list[str]
    cname: list[str]
    soa: list[str]

    def to_dict(self) -> DnsRecordsDict:
        """Convert DNS records to dictionary format."""
        return {
            "A": self.a,
            "AAAA": self.aaaa,
            "MX": self.mx,
            "NS": self.ns,
            "TXT": self.txt,
            "CNAME": self.cname,
            "SOA": self.soa,
        }

    @classmethod
    def from_dict(cls, records: DnsRecordsDict) -> "DnsRecords":
        """Create DNS records from dictionary format."""
        return cls(
            a=records.get("A", []),
            aaaa=records.get("AAAA", []),
            mx=records.get("MX", []),
            ns=records.get("NS", []),
            txt=records.get("TXT", []),
            cname=records.get("CNAME", []),
            soa=records.get("SOA", []),
        )

    def __str__(self) -> str:
        """Return a string representation of DNS records."""
        parts = []
        if self.a:
            parts.append(f"A: {len(self.a)}")
        if self.aaaa:
            parts.append(f"AAAA: {len(self.aaaa)}")
        if self.mx:
            parts.append(f"MX: {len(self.mx)}")
        if self.ns:
            parts.append(f"NS: {len(self.ns)}")
        if self.txt:
            parts.append(f"TXT: {len(self.txt)}")
        if self.cname:
            parts.append(f"CNAME: {len(self.cname)}")
        if self.soa:
            parts.append(f"SOA: {len(self.soa)}")

        return f"DNS Records({', '.join(parts) if parts else 'empty'})"

    @property
    def has_any_records(self) -> bool:
        """Check if any DNS records are present."""
        return bool(self.a or self.aaaa or self.mx or self.ns or self.txt or self.cname or self.soa)
