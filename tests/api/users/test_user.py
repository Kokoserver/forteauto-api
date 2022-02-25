import pytest
from fastapi import status
from fastapi.testclient import TestClient
core.jwt_anth import JWTAUTH
conf import config as base_config
import time


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "first_name, last_name, email, password, phone_number",
    [("test", "test_fort", "test@gamil.com", "12345", "0847324023729"),
     ("test2", None, "test.com", None, "23408473240237"),
     (None, "test_fort", "test@gamil.com", None, False)])
async def test_invalid_registeration(client: TestClient, first_name, last_name,
                                     email, password, phone_number):
    with client as client:
        res = client.post(
            "users/register",
            json={
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password,
                "phone_number": phone_number
            })
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_register(client: TestClient, get_user_data: dict):
    with client as client:
        res = client.post("users/register", json=get_user_data)
        assert res.status_code == status.HTTP_201_CREATED
        assert res.json()["message"] != None


@pytest.mark.asyncio
async def test_account_already_exist(client: TestClient, inactive_user: dict):
    with client as client:
        res = client.post("users/register", json=inactive_user)
        assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_verify_user_email(client: TestClient, inactive_user: dict):
    token = JWTAUTH.DataEncoder(data={"id": inactive_user["id"]})
    with client as client:
        res = client.post("users/activate", json={"token": token})
        assert res.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_user_is_not_activated(client: TestClient, inactive_user: dict):
    with client as client:
        res = client.post(
            "auth/login",
            data={
                "username": inactive_user["email"],
                "password": inactive_user["password"]
            })
        assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_activate_user(client: TestClient, inactive_user: dict):
    with client as client:
        token = JWTAUTH.DataEncoder(
            data={"id": inactive_user["id"]},
            secret_key=base_config.settings.refresh_key)
        res = client.post("users/activate", json={"token": token})
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["message"] != None


@pytest.mark.asyncio
async def test_login(client: TestClient, active_user: dict):
    with client as client:
        res = client.post(
            "auth/login",
            data={
                "username": active_user["email"],
                "password": active_user["password"]
            })
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["token_type"] == "bearer"
        assert res.json()["access_token"] != None
        assert res.json()["refresh_token"] != None


@pytest.mark.asyncio
async def test_refresh_token(client: TestClient, authorize_token: dict):
    with client as client:
        res = client.post(
            "auth/token_refresh",
            json={"refresh_token": authorize_token["refresh_token"]})
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["access_token"] != None
        assert res.json()["refresh_token"] != None
        assert isinstance(res.json()["refresh_token"], str) and isinstance(
            res.json()["access_token"], str)


@pytest.mark.asyncio
async def test_token_expire(client: TestClient, active_user: dict):
    with client as client:
        token = JWTAUTH.DataEncoder(
            data={
                "id": active_user["id"],
                "role": active_user["role"],
                "is_active": active_user["is_active"]
            },
            secret_key=base_config.settings.secret_key,
            seconds=1)
        time.sleep(2)
        res = client.get(
            "users/me",
            headers={
                **client.headers, "Authorization": f"Bearer {token}"
            })
        assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_refresh_token(client: TestClient, authorize_token: dict):
    with client as client:
        res = client.post(
            "auth/token_refresh",
            json={"refresh_token": authorize_token["refresh_token"]})
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["access_token"] != None
        assert res.json()["refresh_token"] != None
        assert isinstance(res.json()["refresh_token"], str) and isinstance(
            res.json()["access_token"], str)


@pytest.mark.asyncio
async def test_expire_refresh_token(client: TestClient, active_user: dict):
    with client as client:
        token = JWTAUTH.DataEncoder(
            data={
                "id": active_user["id"],
                "role": active_user["role"],
                "is_active": active_user["is_active"]
            },
            secret_key=base_config.settings.refresh_key,
            seconds=1)
        time.sleep(2)
        res = client.post("auth/token_refresh", json={"refresh_token":token})
        assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_user_details(client: TestClient, authorize_token: dict,
                                active_user: dict):
    with client as client:
        res = client.get(
            "users/me",
            headers={
                **client.headers, "Authorization":
                    f"Bearer {authorize_token['access_token']}"
            })
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["email"] == active_user["email"]
        assert res.json()["first_name"] == active_user["first_name"]
        assert res.json()["last_name"] == active_user["last_name"]
        assert res.json()["phone_number"] == active_user["phone_number"]


@pytest.mark.asyncio
async def test_account_not_found(
    client: TestClient,
    get_user_data: dict,
):
    with client as client:
        res = client.post(
            "auth/login",
            data={
                "username": get_user_data["email"],
                "password": get_user_data["password"]
            })
        assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_password_reset_link(client: TestClient, inactive_user: dict):
    token = JWTAUTH.DataEncoder(data={"id": inactive_user["id"]})
    with client as client:
        res = client.post("users/activate", json={"token": token})
        assert res.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_reset_password(client: TestClient, active_user: dict):
    token = JWTAUTH.DataEncoder(data={"id": active_user["id"]}, days=1)
    with client as client:
        res = client.put(
            "users/password",
            json={
                "token": token,
                "password": "newpassword",
                "confirm_password": "newpassword"
            })
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["message"] != None


@pytest.mark.asyncio
async def test_delete_user_by_non_admin(authorize_client: TestClient, active_user: dict):
    with authorize_client as client:
        res = client.delete(f"users/{active_user['id']}/remove")
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
        assert res.status_code != status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_delete_user_by_admin(authorize_client_super_admin: TestClient,
                                    active_user):
    with authorize_client_super_admin as client:
        res = client.delete(f"users/{active_user['id']}/remove")
        assert res.status_code == status.HTTP_204_NO_CONTENT
        assert res.status_code != status.HTTP_401_UNAUTHORIZED
