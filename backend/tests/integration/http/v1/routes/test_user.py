import uuid
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


@pytest.mark.asyncio(loop_scope="session")
async def test_get_users_authenticated(client: AsyncClient, auth_user: AuthUser) -> None:
    resp = await client.get("/v1/user/")
    assert resp.status_code == status.HTTP_200_OK

    body = resp.json()
    assert isinstance(body, dict)
    assert "users" in body
    assert isinstance(body["users"], list)

    users = body["users"]
    assert any(u.get("email") == auth_user["email"] for u in users)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_by_id_not_found(client: AsyncClient, auth_user: AuthUser) -> None:
    missing_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    resp = await client.get(f"/v1/user/id/{missing_id}/")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json()["description"] == f"Can't find user by id: {missing_id}"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_by_id_self(client: AsyncClient, auth_user: AuthUser) -> None:
    user_id = auth_user["id"]
    resp = await client.get(f"/v1/user/id/{user_id}/")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    # Response model is ReadUserByIDResponse
    assert data["id"] == user_id
    assert data["email"] == auth_user["email"]
    assert isinstance(data["name"], str)


@pytest.mark.asyncio(loop_scope="session")
async def test_change_user_name(client: AsyncClient, auth_user: AuthUser) -> None:
    user_id = auth_user["id"]
    old_name = auth_user["name"]
    new_name = "Integration-Updated"

    # Change to new name
    resp = await client.patch(f"/v1/user/id/{user_id}/name/", json={"name": new_name})
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    resp = await client.get(f"/v1/user/id/{user_id}/")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["name"] == new_name

    # Revert to old name to keep state stable
    resp = await client.patch(f"/v1/user/id/{user_id}/name/", json={"name": old_name})
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    resp = await client.get(f"/v1/user/id/{user_id}/")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["name"] == old_name


@pytest.mark.asyncio(loop_scope="session")
async def test_change_user_email(client: AsyncClient, auth_user: AuthUser) -> None:
    user_id = auth_user["id"]
    old_email = auth_user["email"]
    new_email = f"tester_new_{uuid.uuid4().hex[:6]}@example.com"

    # Change to new email
    resp = await client.patch(f"/v1/user/{user_id}/email/", json={"email": new_email})
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    resp = await client.get(f"/v1/user/id/{user_id}/")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["email"] == new_email

    # Revert to old email
    resp = await client.patch(f"/v1/user/{user_id}/email/", json={"email": old_email})
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    resp = await client.get(f"/v1/user/id/{user_id}/")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["email"] == old_email


@pytest.mark.asyncio(loop_scope="session")
async def test_change_user_password(client: AsyncClient, auth_user: AuthUser) -> None:
    user_id = auth_user["id"]
    old_password = auth_user["password"]
    new_password = "AnotherSecure1234"

    # Change to new password
    resp = await client.patch(f"/v1/user/id/{user_id}/password", json={"password": new_password})
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    # Re-login with new password to verify password change took effect
    resp = await client.post("/v1/auth/login/", json={"email": auth_user["email"], "password": new_password})
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    # Revert password back to old
    resp = await client.patch(f"/v1/user/id/{user_id}/password", json={"password": old_password})
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    # Re-login with old password to verify
    resp = await client.post("/v1/auth/login/", json={"email": auth_user["email"], "password": old_password})
    assert resp.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_user_self(client: AsyncClient, auth_user: AuthUser) -> None:
    user_id = auth_user["id"]

    resp = await client.delete(f"/v1/user/id/{user_id}/")
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    resp = await client.get(f"/v1/user/id/{user_id}/")
    assert resp.status_code == status.HTTP_403_FORBIDDEN
