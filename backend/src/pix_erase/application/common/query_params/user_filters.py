from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True, kw_only=True)
class UserQueryFilters:
    email: str | None = field(default=None)
    name: str | None = field(default=None)
