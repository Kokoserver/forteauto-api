from typing import List, Optional, Union
from fastapi import APIRouter, Depends, status, HTTPException, Response
import ormar
from fortauto.api.api_base_schema import Message
from fortauto.api.service.listing.service_listing_model import Service_type
from fortauto.api.user.property.user_property_model import Car
from fortauto.api.user.user_model import User
from fortauto.api.service.service_model import Service, Service_status
from fortauto.api.service.service_schema import ServiceInput, ServiceOutput, ServiceUpdate
from fortauto.core.authentication import UserWrite

router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=ServiceOutput)
async def create_service(new_service_data: ServiceInput,
                         user:int = Depends(UserWrite.current_user)):
    # try:
    get_service_type: Service_type = await Service_type.objects.get_or_none(
        id=new_service_data.service_type)
    if not get_service_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"service type with name:{new_service_data.service_type} does not exist"
        )

    car_type: Car = await Car.objects.get_or_none(
        ormar.and_(vin_number__icontains=new_service_data.car_type.vin_number),
        ormar.and_(maker__icontains=new_service_data.car_type.maker),
        ormar.and_(maker__icontains=new_service_data.car_type.maker),
        owner=user)

    car_to_be_repaired: Car = car_type if car_type else await Car(
        **new_service_data.car_type.dict(), owner=user).save()
    new_service_data.car_type = car_to_be_repaired.id
    new_service_obj: Service = await Service(
        **new_service_data.dict(), owner=user).save()
    if "others" in get_service_type.name.split():
        return Message(
            message="Service was added succesfully, we will get back to you as soon as possible"
        )
    data_output = await Service.objects.select_related(
        ["service_type", "car_type"]).get_or_none(id=new_service_obj.id)
    return data_output


@router.put(
    "/{service_id}",
    status_code=status.HTTP_200_OK,
    response_model=ServiceOutput)
async def update_service(service_id: int,
                         service_data: ServiceUpdate,
                         user:int = Depends(UserWrite.current_user)):
    get_service: Service = await Service.objects.get_or_none(id=service_id, owner=user)
    if not get_service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"service type with name:{service_data.service_type} does not exist"
        )
    # TODO ask Mr. Mike
    if get_service.status == Service_status.picked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot update a completed service")

    get_service_type: Service_type = await Service_type.objects.get_or_none(
        id=service_data.service_type)
    if not get_service_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"service type with name:{service_data.service_type} does not exist"
        )

    car_type: Car = await Car.objects.get_or_none(
        ormar.or_(model__icontains=service_data.car_type.model),
        ormar.or_(vin_number__icontains=service_data.car_type.vin_number),
        ormar.or_(maker__icontains=service_data.car_type.maker),
        owner=user)
    car_to_be_repaired: Car = car_type if car_type else await Car(
        **service_data.car_type.dict(exclude_unset=True), owner=user).save()
    service_data.car_type = car_to_be_repaired.id
    new_service_obj: Service = await get_service.update(
        **service_data.dict(), owner=user)
    if "others" in get_service_type.name.split():
        return Message(
            message="Service was updated succesfully, we will get back to you as soon as possible"
        )
    data_output = await Service.objects.select_related(
        ["service_type", "car_type"]).get_or_none(id=new_service_obj.id)
    return data_output


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[ServiceOutput])
async def get_service_list(user:int = Depends(UserWrite.current_user),
                           limit: Optional[int] = 10,
                           skip: Optional[int] = 0):
    all_user_services = await Service.objects.select_related(
        ["service_type",
         "car_type"]).filter(owner=user).limit(limit).offset(skip).all()
    if all_user_services:
        return all_user_services
    return []


@router.get(
    "/{service_id}",
    status_code=status.HTTP_200_OK,
    response_model=ServiceOutput)
async def get_service_list(service_id: int,
                           user:int = Depends(UserWrite.current_user)):
    service_obj: Service = await Service.objects.select_related(
        ["service_type", "car_type"]).get_or_none(
            id=service_id, owner=user)
    if service_obj:
        return service_obj
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="service does not exist")


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(service_id: int,
                         user:int = Depends(UserWrite.current_user)):
    service_obj = await Service.objects.get_or_none(id=service_id, owner=user)
    if service_obj:
        await service_obj.delete()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"service with id:{service_id} does not exist")
