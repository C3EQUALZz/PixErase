import uuid

import pytest
from httpx import AsyncClient, ASGITransport
from starlette import status
from fastapi import FastAPI

from tests.integration.http.v1.routes.conftest import AuthUser


@pytest.mark.asyncio(loop_scope="session")
async def test_signup_success(client: AsyncClient) -> None:
    email = f"auth_sign_{uuid.uuid4().hex[:8]}@example.com"
    payload = {"email": email, "name": "Auth-Tester", "password": "SignUpPass123"}

    resp = await client.post("/v1/auth/signup/", json=payload)
    assert resp.status_code == status.HTTP_201_CREATED
    data = resp.json()
    assert "id" in data


@pytest.mark.asyncio(loop_scope="session")
async def test_signup_duplicate_email_conflict(client: AsyncClient) -> None:
    email = f"dup_{uuid.uuid4().hex[:8]}@example.com"
    payload = {"email": email, "name": "Duplicate", "password": "DupPass123"}

    resp1 = await client.post("/v1/auth/signup/", json=payload)
    assert resp1.status_code == status.HTTP_201_CREATED

    resp2 = await client.post("/v1/auth/signup/", json=payload)
    assert resp2.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio(loop_scope="session")
async def test_login_success_sets_cookie(client: AsyncClient) -> None:
    email = f"login_{uuid.uuid4().hex[:8]}@example.com"
    password = "LoginPass123!"

    resp = await client.post("/v1/auth/signup/", json={"email": email, "name": "Login-OK", "password": password})
    assert resp.status_code == status.HTTP_201_CREATED

    resp = await client.post("/v1/auth/login/", json={"email": email, "password": password})
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    # httpx client keeps cookies set by ASGITransport; ensure access_token present
    assert "access_token" in client.cookies


@pytest.mark.asyncio(loop_scope="session")
async def test_login_wrong_password_unauthorized(app: FastAPI) -> None:
    # Use isolated client with its own cookie jar to avoid interfering with session client
    transport = ASGITransport(app)
    async with AsyncClient(transport=transport, base_url="http://test") as local:
        email = f"login_fail_{uuid.uuid4().hex[:8]}@example.com"
        resp = await local.post(
            "/v1/auth/signup/", json={"email": email, "name": "Login-Fail", "password": "RightPass123"}
        )
        assert resp.status_code == status.HTTP_201_CREATED

        resp = await local.post("/v1/auth/login/", json={"email": email, "password": "WrongPass123"})
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio(loop_scope="session")
async def test_read_me_authenticated(client: AsyncClient, auth_user: AuthUser) -> None:
    resp = await client.get("/v1/auth/me/")
    assert resp.status_code == status.HTTP_200_OK
    me = resp.json()
    assert me["email"] == auth_user["email"]
    assert me["id"] == auth_user["id"]


@pytest.mark.asyncio(loop_scope="session")
async def test_logout_then_me_requires_auth(client: AsyncClient, auth_user: AuthUser) -> None:
    # Ensure logged in (fixture already did), call logout
    resp = await client.delete("/v1/auth/logout/")
    # Depending on implementation, logout may return 204 or 401 if already logged out
    assert resp.status_code in (status.HTTP_204_NO_CONTENT, status.HTTP_401_UNAUTHORIZED)

    resp = await client.get("/v1/auth/me/")
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    # Re-login to restore state for other tests
    resp = await client.post(
        "/v1/auth/login/", json={"email": auth_user["email"], "password": auth_user["password"]}
    )
    assert resp.status_code == status.HTTP_204_NO_CONTENT
