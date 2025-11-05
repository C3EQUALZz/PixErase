from typing import TypedDict

import pytest
from httpx import AsyncClient
from starlette import status


class AuthUser(TypedDict):
    id: str
    email: str
    name: str
    password: str


@pytest.fixture(scope="session")
async def auth_user(client: AsyncClient) -> AuthUser:
    email = "tester_5cee45b@example.com"
    password = "SuperSecure123"
    name = "Integration-Tester"

    signup_payload = {"email": email, "name": name, "password": password}
    signup_resp = await client.post("/v1/auth/signup/", json=signup_payload)
    assert signup_resp.status_code == status.HTTP_201_CREATED
    created = signup_resp.json()
    assert "id" in created

    login_payload = {"email": email, "password": password}
    login_resp = await client.post("/v1/auth/login/", json=login_payload)
    assert login_resp.status_code == status.HTTP_204_NO_CONTENT

    return {"id": created["id"], "email": email, "name": name, "password": password}
