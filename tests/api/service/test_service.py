import pytest
from fastapi.testclient import TestClient
from fastapi import status

@pytest.mark.asyncio
async def test_get_all_service(authorize_client: TestClient,
                               new_user_servce: dict):
    with authorize_client as client:
        res = client.get("services/")
        assert isinstance(res.json(), list)
        assert new_user_servce["id"] == res.json()[0]["id"]
        assert new_user_servce["serviceId"] == res.json(
        )[0]["serviceId"]
        assert new_user_servce["additional_notes"] == res.json(
        )[0]["additional_notes"]
        assert new_user_servce["quantity"] == res.json()[0]["quantity"]


@pytest.mark.asyncio
async def test_get_filtering_services(authorize_client: TestClient,
                                      new_user_servce):
    with authorize_client as client:
        res = client.get(f"services/?q={new_user_servce['serviceId']}")
        assert isinstance(res.json(), list)
        assert new_user_servce["id"] == res.json()[0]["id"]
        assert new_user_servce["serviceId"] == res.json()[0]["serviceId"]
        assert new_user_servce["quantity"] == res.json()[0]["quantity"]
        assert new_user_servce["additional_notes"] == res.json(
        )[0]["additional_notes"]


@pytest.mark.asyncio
async def test_get_pagination_service(authorize_client: TestClient,
                                      new_user_servce: dict):
    with authorize_client as client:
        res = client.get(f"services/?limit=1&skip=0")
        assert isinstance(res.json(), list)
        assert new_user_servce["id"] == res.json()[0]["id"]
        assert new_user_servce["serviceId"] == res.json()[0]["serviceId"]
        assert new_user_servce["quantity"] == res.json()[0]["quantity"]
        assert new_user_servce["additional_notes"] == res.json(
        )[0]["additional_notes"]


@pytest.mark.asyncio
async def test_get_single_service(authorize_client: TestClient,
                                  new_user_servce: dict):
    with authorize_client as client:
        res = client.get(f"services/{new_user_servce['id']}")
        assert new_user_servce["id"] == res.json()["id"]
        assert new_user_servce["serviceId"] == res.json()["serviceId"]
        assert new_user_servce["quantity"] == res.json()["quantity"]
        assert new_user_servce["additional_notes"] == res.json(
        )["additional_notes"]


@pytest.mark.asyncio
async def test_update_single_service(authorize_client: TestClient,
                                     new_user_servce: dict,
                                     new_user_property: dict,
                                     new_servce_listing: dict):
    with authorize_client as client:
        new_data_to_update = {
            "car_type": new_user_property,
            "service_type": new_servce_listing["id"],
            "additional_notes": "new updated services",
            "quantity": 5,
            "status": "repairing"
        }
        res = client.put(
            f"services/{new_user_servce['id']}", json=new_data_to_update)
        assert res.json()["id"] == new_user_servce["id"]
        assert res.json()["serviceId"] == new_user_servce["serviceId"]
        assert res.json()["quantity"] == new_data_to_update["quantity"]
        assert res.json()["additional_notes"] == new_data_to_update["additional_notes"]


@pytest.mark.asyncio
async def test_remove_single_service(authorize_client: TestClient, new_user_servce:dict):
    with authorize_client as client:
        res = client.delete(f"services/{new_user_servce['id']}")
        assert res.status_code == status.HTTP_204_NO_CONTENT
