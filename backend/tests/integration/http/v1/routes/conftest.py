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

    # Ensure we start from a clean auth state to avoid 403 on signup
    await client.delete("/v1/auth/logout/")

    signup_payload = {"email": email, "name": name, "password": password}
    signup_resp = await client.post("/v1/auth/signup/", json=signup_payload)

    if signup_resp.status_code == status.HTTP_201_CREATED:
        created = signup_resp.json()
        assert "id" in created
    elif signup_resp.status_code == status.HTTP_409_CONFLICT:
        # User already exists in current DB/session; fetch id via login + read_me
        login_resp = await client.post("/v1/auth/login/", json={"email": email, "password": password})
        assert login_resp.status_code == status.HTTP_204_NO_CONTENT
        me_resp = await client.get("/v1/auth/me/")
        assert me_resp.status_code == status.HTTP_200_OK
        created = {"id": me_resp.json()["id"]}
    else:
        assert False, f"Unexpected signup status: {signup_resp.status_code}, body: {signup_resp.text}"

    # Ensure authenticated for subsequent tests
    login_payload = {"email": email, "password": password}
    login_resp = await client.post("/v1/auth/login/", json=login_payload)
    assert login_resp.status_code == status.HTTP_204_NO_CONTENT

    return {"id": created["id"], "email": email, "name": name, "password": password}
