import pytest
from fastapi.testclient import TestClient
from fastapi import status



@pytest.mark.asyncio
async def test_invalid_create_address(authorize_client: TestClient):
    with authorize_client as client:
        res = client.post(
            "address/",
            json={
                "state": None,
                "city": False,
                "address": "2 thumpson str, off akerele",
                "nearest_bus_stop": "shitta"
            })
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_all_user_address(authorize_client: TestClient, new_user_address:dict):
    with authorize_client as client:
        res = client.get("address/")
        assert isinstance(res.json(), list)
        assert new_user_address["id"] == res.json()[0]["id"]
        assert new_user_address["state"] == res.json()[0]["state"]
        assert new_user_address["city"] == res.json()[0]["city"]
        assert new_user_address["address"] == res.json()[0]["address"]
        assert new_user_address["nearest_bus_stop"] == res.json(
        )[0]["nearest_bus_stop"]


@pytest.mark.asyncio
async def test_get_single_user_address(authorize_client: TestClient, new_user_address:dict):
    with authorize_client as client:
        res = client.get(f"address/{new_user_address['id']}")
        assert new_user_address["state"] == res.json()["state"]
        assert new_user_address["city"] == res.json()["city"]
        assert new_user_address["address"] == res.json()["address"]
        assert new_user_address["nearest_bus_stop"] == res.json()["nearest_bus_stop"]


@pytest.mark.asyncio
async def test_update_single_user_address(authorize_client: TestClient, new_user_address:dict):
    with authorize_client as client:
        new_data_to_update = {
            "state": "ibadan",
            "city": "malete",
            "address": "2 thumpson str, off akerele",
            "nearest_bus_stop": "shitta"
        }
        res = client.put(
            f"address/{new_user_address['id']}", json=new_data_to_update)
        assert new_user_address["id"] == res.json()["id"]
        assert new_data_to_update["state"] == res.json()["state"]
        assert new_data_to_update["city"] == res.json()["city"]
        assert new_data_to_update["address"] == res.json()["address"]
        assert new_data_to_update["nearest_bus_stop"] == res.json(
        )["nearest_bus_stop"]


@pytest.mark.asyncio
async def test_remove_single_user_address(authorize_client: TestClient, new_user_address:dict):
    with authorize_client as client:
        res2 = client.delete(f"address/{new_user_address['id']}")
        assert res2.status_code == status.HTTP_204_NO_CONTENT
