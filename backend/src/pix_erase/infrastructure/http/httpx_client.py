import logging
from typing import Any, Final, override

import httpx
from httpx import Response
from tenacity import retry, stop_after_attempt, wait_exponential

from pix_erase.infrastructure.errors.http import HttpError
from pix_erase.infrastructure.http.base import HttpClient, HttpHeaders, HttpResponse, QueryParams

logger: Final[logging.Logger] = logging.getLogger(__name__)


class HttpxHttpClient(HttpClient):
    def __init__(
        self,
        httpx_client: httpx.AsyncClient,
    ) -> None:
        self._client: Final[httpx.AsyncClient] = httpx_client

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
    )
    @override
    async def get(
        self,
        url: str,
        *,
        params: QueryParams | None = None,
        headers: HttpHeaders | None = None,
        timeout: float | None = None,
    ) -> HttpResponse:
        try:
            logger.debug(
                "Started get request to url: %s with params: %s and headers: %s and timeout: %s",
                url,
                params,
                headers,
                timeout,
            )
            response: Response = await self._client.get(
                url,
                params=params,
                headers=headers,
                timeout=timeout,
            )

            logger.debug(
                "Got request from url: %s with params: %s and headers: %s and timeout: %s",
            )

            return HttpResponse(
                url=str(response.url),
                status_code=response.status_code,
                headers=dict(response.headers),
                content=response.content,
            )
        except (httpx.TransportError, httpx.HTTPError) as exc:
            msg = f"Can't request url: {url} for get method"
            msg_for_log = (
                f"Can't request {url} for get method with request to url: "
                f"%s with params: %s and headers: %s and timeout: %s"
            )
            logger.exception(msg_for_log)
            raise HttpError(msg) from exc

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
    )
    @override
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
        try:
            response: Response = await self._client.post(
                url,
                params=params,
                headers=headers,
                json=json_like,
                data=data,
                timeout=timeout,
            )
            return HttpResponse(
                url=str(response.url),
                status_code=response.status_code,
                headers=dict(response.headers),
                content=response.content,
            )
        except (httpx.TransportError, httpx.HTTPError) as exc:
            msg = f"Can't request url {url} for post method"
            msg_for_log = (
                f"Can't request {url} for post method with request to url: "
                f"%s with params: %s and headers: %s and timeout: %s"
            )
            logger.exception(msg_for_log)
            raise HttpError(msg) from exc

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
    )
    @override
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
        try:
            response: Response = await self._client.put(
                url,
                params=params,
                headers=headers,
                json=json_like,
                data=data,
                timeout=timeout,
            )
            return HttpResponse(
                url=str(response.url),
                status_code=response.status_code,
                headers=dict(response.headers),
                content=response.content,
            )
        except (httpx.TransportError, httpx.HTTPError) as exc:
            msg = f"Can't request {url} for put method"
            msg_for_log = (
                f"Can't request {url} for put method with request to url: "
                f"%s with params: %s and headers: %s and timeout: %s"
            )
            logger.exception(msg_for_log)
            raise HttpError(msg) from exc

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
    )
    @override
    async def delete(
        self,
        url: str,
        *,
        params: QueryParams | None = None,
        headers: HttpHeaders | None = None,
        timeout: float | None = None,
    ) -> HttpResponse:
        try:
            response: Response = await self._client.delete(
                url,
                params=params,
                headers=headers,
                timeout=timeout,
            )
            return HttpResponse(
                url=str(response.url),
                status_code=response.status_code,
                headers=dict(response.headers),
                content=response.content,
            )
        except (httpx.TransportError, httpx.HTTPError) as exc:
            msg = f"Can't request {url} for delete method"
            msg_for_log = (
                f"Can't request {url} for delete method with request to url: "
                f"%s with params: %s and headers: %s and timeout: %s"
            )
            logger.exception(msg_for_log)
            raise HttpError(msg) from exc
