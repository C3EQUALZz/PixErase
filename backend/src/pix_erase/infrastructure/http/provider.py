from typing import AsyncIterator

import httpx

from pix_erase.setup.config.http import HttpClientConfig


async def get_httpx_client(http_client_config: HttpClientConfig) -> AsyncIterator[httpx.AsyncClient]:
    cert: str | tuple[str, str] | None
    if http_client_config.client_cert_path and http_client_config.client_key_path:
        cert = (http_client_config.client_cert_path, http_client_config.client_key_path)
    elif http_client_config.client_cert_path:
        cert = http_client_config.client_cert_path
    else:
        cert = None

    limits: httpx.Limits = httpx.Limits(
        max_connections=http_client_config.max_connections,
        max_keepalive_connections=http_client_config.max_keepalive_connections,
        keepalive_expiry=http_client_config.keepalive_expiry,
    )

    async with httpx.AsyncClient(
        timeout=http_client_config.default_timeout,
        verify=http_client_config.verify,
        cert=cert,
        follow_redirects=http_client_config.follow_redirects,
        http2=http_client_config.http2,
        proxy=http_client_config.proxy,
        limits=limits,
        trust_env=False,
    ) as client:
        yield client


