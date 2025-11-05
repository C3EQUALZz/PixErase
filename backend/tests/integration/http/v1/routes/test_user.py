import uuid
from typing import TypedDict

import pytest
from httpx import AsyncClient
from starlette import status


class AuthUser(TypedDict):
    id: str
    email: str
    name: str


@pytest.fixture(scope="session")
async def auth_user(client: AsyncClient) -> AuthUser:
    email = f"tester_{uuid.uuid4().hex[:8]}@example.com"
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

    return {"id": created["id"], "email": email, "name": name}


@pytest.mark.asyncio(loop_scope="session")
async def test_get_users_authenticated(client: AsyncClient, auth_user: AuthUser) -> None:
    resp = await client.get("/v1/user/")
    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()
    assert isinstance(body, dict)
    assert "users" in body and isinstance(body["users"], list)

    users = body["users"]
    assert any(u.get("email") == auth_user["email"] for u in users)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_by_id_not_found(client: AsyncClient, auth_user: AuthUser) -> None:
    missing_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    resp = await client.get(f"/v1/user/id/{missing_id}/")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json()["description"] == f"Can't find user by id: {missing_id}"
