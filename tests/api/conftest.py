import pytest
from fastapi.testclient import TestClient
from forteauto.core.jwt_anth import JWTAUTH
from forteauto.database import database_dependencies
from forteauto.api.user import user_model

from forteauto.api.user.address.user_address_model import Address
from forteauto.api.user.property.user_property_model import Car
from forteauto.database import database_dependencies
from forteauto.api.service.listing.service_listing_model import Service_type
from forteauto.api.service.service_model import Service

@pytest.fixture
def get_user_data_map():
    _user_data_map: dict = {
        "test_user": {
            "email": "test@gmail.com",
            "password": "test12345",
            "first_name":"active",
            "last_name":"active_test",
            "phone_number":"08089223645"
        }
    }
    return _user_data_map


@pytest.fixture
def get_user_data(get_user_data_map):
    _active_user_data: dict = get_user_data_map.get("test_user")
    return _active_user_data


@pytest.fixture
@pytest.mark.asyncio
async def new_user(get_user_data):
    async with database_dependencies.database:
        user = user_model.User(**get_user_data)
        user.hash_password()
        user_data_obj = await user.save()
        get_user_data["id"] = user_data_obj.id
        get_user_data["role"] = user_data_obj.role
        get_user_data["is_active"] = user_data_obj.is_active
    assert user_data_obj.is_active == False
    return get_user_data, user_data_obj


@pytest.fixture
@pytest.mark.asyncio
async def inactive_user(new_user):
    async with database_dependencies.database:
        user_data, user_obj = new_user
    assert user_obj.is_active == False
    assert user_obj.role == user_model.UserRole.default
    assert user_data["role"] == user_model.UserRole.default
    return user_data

@pytest.fixture
@pytest.mark.asyncio
async def active_user(new_user):
    async with database_dependencies.database:
        user_data, user_obj = new_user
        active_user_data = await user_obj.update(is_active=True, role=user_model.UserRole.default)
        user_data["role"] = user_model.UserRole.default
        user_data["is_active"] = True
    assert active_user_data.role == user_model.UserRole.default
    assert active_user_data.is_active == True
    assert user_data["role"] == user_model.UserRole.default
    assert user_data["is_active"] == True
    return user_data


@pytest.fixture
@pytest.mark.asyncio
async def admin_user(new_user):
    async with database_dependencies.database:
        user_data, user_obj = new_user
        await user_obj.update(role=user_model.UserRole.admin, is_active=True)
        user_data["role"] = user_model.UserRole.admin
        user_data["is_active"] = True
    assert user_obj.role == user_model.UserRole.admin
    assert user_data["is_active"] == True
    assert user_obj.role == user_model.UserRole.admin
    assert user_obj.is_active == True
    return user_data

@pytest.fixture
@pytest.mark.asyncio
async def super_user(new_user):
    async with database_dependencies.database:
        user_data, user_obj = new_user
        await user_obj.update(role=user_model.UserRole.super_admin, is_active=True)
        user_data["role"] = user_model.UserRole.super_admin
    assert user_obj.role == user_model.UserRole.super_admin
    assert user_obj.is_active == True
    assert user_data["role"] == user_model.UserRole.super_admin
    return user_data

@pytest.fixture
async def authorize_token(active_user):
        access_token, refresh_token = JWTAUTH.JwtEncoder(
            data={
                "id": active_user["id"],
                "role": active_user["role"],
                "is_active": active_user["is_active"]
            }
        )
        assert access_token != None
        assert refresh_token != None
        return {"access_token":access_token, "refresh_token":refresh_token}

@pytest.fixture
@pytest.mark.asyncio
async def authorize_token_admin(admin_user):
        access_token, refresh_token = JWTAUTH.JwtEncoder(
            data={
                "id": admin_user["id"],
                "role": admin_user["role"],
                "is_active": admin_user["is_active"]
            }
        )
        assert access_token != None
        assert refresh_token != None
        return {"access_token":access_token, "refresh_token":refresh_token}

@pytest.fixture
@pytest.mark.asyncio
async def authorize_token_super(super_user):
        access_token, refresh_token = JWTAUTH.JwtEncoder(
            data={
                "id": super_user["id"],
                "role": super_user["role"],
                "is_active": super_user["is_active"]
            }
        )
        assert access_token != None
        assert refresh_token != None
        return {"access_token":access_token, "refresh_token":refresh_token}

@pytest.fixture
@pytest.mark.asyncio
async def authorize_client(client:TestClient, authorize_token:dict):
        client.headers = {
            **client.headers,
            "Authorization": f"Bearer {authorize_token['access_token']}"
        }
        return client

@pytest.fixture
@pytest.mark.asyncio
async def authorize_client_admin(client:TestClient, authorize_token_admin:dict):
        client.headers = {
            **client.headers,
            "Authorization": f"Bearer {authorize_token_admin['access_token']}"
        }
        return client

@pytest.fixture
@pytest.mark.asyncio
async def authorize_client_super_admin(client:TestClient, authorize_token_super:dict):
        client.headers = {
            **client.headers,
            "Authorization": f"Bearer {authorize_token_super['access_token']}"
        }
        return client


# ahdweoh


_test_user_address = {
    "state": "lagos",
    "city": "surulere",
    "address": "2 thumpson str, off akerele",
    "nearest_bus_stop": "shitta"
}

_test_user_car = {
    "maker": "toyota",
    "vin_number": "8242394jasasas",
    "model": "avalon2012"
}

@pytest.fixture
@pytest.mark.asyncio
async def new_user_property(active_user: dict):
    async with database_dependencies.database:
        new_property = Car(**_test_user_car, owner=active_user["id"])
        await new_property.save()
        assert new_property.id != None
        assert new_property.maker == _test_user_car["maker"]
        assert new_property.model == _test_user_car["model"]
        assert new_property.vin_number == _test_user_car["vin_number"]
        return new_property.dict(exclude={"owner", "services"})


@pytest.fixture
@pytest.mark.asyncio
async def new_user_address(active_user: dict):
    async with database_dependencies.database:
        new_address = Address(**_test_user_address, owner=active_user["id"])
        await new_address.save()
        assert new_address.id != None
        assert new_address.state == _test_user_address["state"]
        assert new_address.city == _test_user_address["city"]
        assert new_address.address == _test_user_address["address"]
        assert new_address.nearest_bus_stop == _test_user_address[
            "nearest_bus_stop"]
        return new_address.dict()



_test_service_listing = {
    "name": "quick",
    "description": "jdsjsfsiodjfposdjfspdofjspofjso",
    "price": 2000
}

_test_service = {"additional_notes": "something", "quantity": 1}


@pytest.fixture
@pytest.mark.asyncio
async def new_servce_listing():
    async with database_dependencies.database:
        new_listing = Service_type(**_test_service_listing)
        await new_listing.save()
        assert new_listing.id != None
        assert new_listing.name == _test_service_listing["name"]
        assert new_listing.description == _test_service_listing["description"]
        assert new_listing.price == _test_service_listing["price"]
        return new_listing.dict()


@pytest.fixture
@pytest.mark.asyncio
async def new_user_servce(active_user, new_user_property, new_servce_listing):
    async with database_dependencies.database:
        new_servce = Service(
            **_test_service,
            car_type=new_user_property,
            service_type=new_servce_listing["id"],
            owner=active_user["id"])
        await new_servce.save()
        assert new_servce.id != None
        assert new_servce.additional_notes == _test_service["additional_notes"]
        assert new_servce.quantity == _test_service["quantity"]
        return new_servce.dict()