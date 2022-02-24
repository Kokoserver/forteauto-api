import pytest
from fastapi.testclient import TestClient
from fastapi import status


@pytest.mark.asyncio
async def test_invalid_create_listings(
        authorize_client_super_admin: TestClient):
    with authorize_client_super_admin as client:
        res = client.post(
            "listings/",
            json={
                "name": "quickkjdshdj",
                "description": "jdsjsfsiodjfposdjfspdofjspofjso",
                "price": True
            })
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_all_listings(authorize_client_super_admin: TestClient,
                                new_servce_listing: dict):
    with authorize_client_super_admin as client:
        res = client.get("listings/")
        assert isinstance(res.json(), list)
        assert new_servce_listing["id"] == res.json()[0]["id"]
        assert new_servce_listing["name"] == res.json()[0]["name"]
        assert new_servce_listing["description"] == res.json()[0]["description"]
        assert new_servce_listing["price"] == res.json()[0]["price"]


@pytest.mark.asyncio
async def test_get_filtering_listing(authorize_client_super_admin: TestClient,
                                     new_servce_listing: dict):
    with authorize_client_super_admin as client:
        res = client.get(f"listings/?q={new_servce_listing['name'][:3]}")
        assert isinstance(res.json(), list)
        assert new_servce_listing["id"] == res.json()[0]["id"]
        assert new_servce_listing["name"] == res.json()[0]["name"]
        assert new_servce_listing["description"] == res.json()[0]["description"]
        assert new_servce_listing["price"] == res.json()[0]["price"]


@pytest.mark.asyncio
async def test_get_pagination_listings(authorize_client_super_admin: TestClient,
                                       new_servce_listing: dict):
    with authorize_client_super_admin as client:
        res = client.get(f"listings/?limit=1&skip=0")
        assert isinstance(res.json(), list)
        assert new_servce_listing["id"] == res.json()[0]["id"]
        assert new_servce_listing["name"] == res.json()[0]["name"]
        assert new_servce_listing["description"] == res.json()[0]["description"]
        assert new_servce_listing["price"] == res.json()[0]["price"]


@pytest.mark.asyncio
async def test_get_single_listings(authorize_client_super_admin: TestClient,
                                   new_servce_listing: dict):
    with authorize_client_super_admin as client:
        res = client.get(f"listings/{new_servce_listing['id']}")
        assert res.json()["name"] == new_servce_listing["name"]
        assert res.json()["description"] == new_servce_listing["description"]
        assert res.json()["price"] == new_servce_listing["price"]


@pytest.mark.asyncio
async def test_update_single_listings(authorize_client_super_admin: TestClient,
                                      new_servce_listing: dict):
    with authorize_client_super_admin as client:
        new_data_to_update = {
            "name": "quick",
            "description": "jdsjsfsiodjfposdjfspdofjspofjso updated",
            "price": 3000
        }
        res = client.put(
            f"listings/{new_servce_listing['id']}", json=new_data_to_update)
        assert res.json()["id"] == new_servce_listing["id"]
        assert res.json()["name"] == new_data_to_update["name"]
        assert res.json()["description"] == new_data_to_update["description"]
        assert res.json()["price"] == new_data_to_update["price"]


@pytest.mark.asyncio
async def test_remove_single_listings(authorize_client_super_admin: TestClient,
                                      new_servce_listing: dict):
    with authorize_client_super_admin as client:
        res2 = client.delete(f"listings/{new_servce_listing['id']}")
        assert res2.status_code == status.HTTP_204_NO_CONTENT
