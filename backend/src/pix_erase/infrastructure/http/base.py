import json
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Mapping, MutableMapping, Protocol, Sequence, runtime_checkable

HttpHeaders = Mapping[str, str]
MutableHttpHeaders = MutableMapping[str, str]

# Each query item can be a scalar or a sequence of scalars for repeated keys
QueryValue = str | int | float | bool
QueryParamItem = QueryValue | Sequence[QueryValue]
QueryParams = Mapping[str, QueryParamItem] | Sequence[tuple[str, QueryValue]]


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
            json: Any | None = None,
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
            json: Any | None = None,
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
