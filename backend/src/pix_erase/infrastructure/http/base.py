import json
from abc import abstractmethod
from dataclasses import dataclass
from collections.abc import Mapping, MutableMapping, Sequence
from typing import Any, Protocol, runtime_checkable

HttpHeaders = Mapping[str, str]
MutableHttpHeaders = MutableMapping[str, str]

# Each query item can be a scalar or a sequence of scalars for repeated keys
_QueryScalar = str | int | float | bool | None
_QueryValue = _QueryScalar | Sequence[_QueryScalar]

# Align with httpx's accepted types:
# - Mapping[str, scalar or sequence of scalars]
# - list[tuple[str, scalar]]
# - tuple[tuple[str, scalar], ...]
QueryParams = (
    Mapping[str, _QueryValue]
    | list[tuple[str, _QueryScalar]]
    | tuple[tuple[str, _QueryScalar], ...]
)


@dataclass(slots=True)
class HttpResponse:
    url: str
    status_code: int
    headers: HttpHeaders
    content: bytes

    @property
    def text(self, encoding: str | None = None) -> str:
        if encoding is not None:
            return self.content.decode(encoding, errors="replace")
        try:
            return self.content.decode()
        except UnicodeDecodeError:
            return self.content.decode("utf-8", errors="replace")

    @property
    def json(self) -> Any:
        return json.loads(self.content)


@runtime_checkable
class HttpClient(Protocol):
    @abstractmethod
    async def get(
            self,
            url: str,
            *,
            params: QueryParams | None = None,
            headers: HttpHeaders | None = None,
            timeout: float | None = None,
    ) -> HttpResponse:
        ...

    @abstractmethod
    async def post(
            self,
            url: str,
            *,
            params: QueryParams | None = None,
            headers: HttpHeaders | None = None,
            json_like: Any | None = None,
            data: Any | None = None,
            timeout: float | None = None,
    ) -> HttpResponse:
        ...

    @abstractmethod
    async def put(
            self,
            url: str,
            *,
            params: QueryParams | None = None,
            headers: HttpHeaders | None = None,
            json_like: Any | None = None,
            data: Any | None = None,
            timeout: float | None = None,
    ) -> HttpResponse:
        ...

    @abstractmethod
    async def delete(
            self,
            url: str,
            *,
            params: QueryParams | None = None,
            headers: HttpHeaders | None = None,
            timeout: float | None = None,
    ) -> HttpResponse:
        ...
