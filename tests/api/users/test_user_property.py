import pytest
from fastapi.testclient import TestClient
from fastapi import status


@pytest.mark.asyncio
@pytest.mark.parametrize("maker, vin_number, model",
                         [("toyota", 12, "avalon2012"),
                          (None, 23, "avalon2013"),
                          ("toyota", "8242394j", True)])
async def test_invalid_create_car(authorize_client: TestClient, maker,
                                  vin_number, model):
    with authorize_client as client:
        res = client.post(
            "cars/",
            json={
                "maker": maker,
                "vin_number": vin_number,
                "model": model
            })
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_all_user_cars(authorize_client: TestClient,
                                 new_user_property: dict):
    with authorize_client as client:
        res = client.get("cars/")
        assert isinstance(res.json(), list)
        assert res.json()[0]["id"] == new_user_property["id"]
        assert res.json()[0]["maker"] == new_user_property["maker"]
        assert res.json()[0]["vin_number"] == new_user_property["vin_number"]
        assert res.json()[0]["model"] == new_user_property["model"]


@pytest.mark.asyncio
async def test_get_single_user_cars(authorize_client: TestClient,
                                    new_user_property: dict):
    with authorize_client as client:
        res = client.get(f"cars/{new_user_property['id']}")
        assert res.json()["id"] == new_user_property["id"]
        assert res.json()["maker"] == new_user_property["maker"]
        assert res.json()["vin_number"] == new_user_property["vin_number"]
        assert res.json()["model"] == new_user_property["model"]


@pytest.mark.asyncio
async def test_update_single_user_car(authorize_client: TestClient,
                                      new_user_property: dict):
    with authorize_client as client:
        new_data_to_update = {
            "maker": "toyota1",
            "vin_number": "8242394jasasa1s",
            "model": "avalon2012"
        }
        res = client.put(
            f"cars/{new_user_property['id']}", json=new_data_to_update)
        assert new_user_property["id"] == res.json()["id"]
        assert new_data_to_update["maker"] == res.json()["maker"]
        assert new_data_to_update["vin_number"] == res.json()["vin_number"]
        assert new_data_to_update["model"] == res.json()["model"]


@pytest.mark.asyncio
async def test_remove_single_user_car(authorize_client: TestClient,
                                      new_user_property: dict):
    with authorize_client as client:
        res = client.delete(f"cars/{new_user_property['id']}")
        assert res.status_code == status.HTTP_204_NO_CONTENT
