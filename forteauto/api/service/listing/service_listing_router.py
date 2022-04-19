from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status
import ormar
from forteauto.core.authentication import UserWrite
from forteauto.api.service.listing.service_listing_model import Service_type
from forteauto.api.service.listing.service_listing_schema import Service_typeInput, Service_typeOutput

router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=Service_typeOutput)
async def create_service(new_service_type: Service_typeInput,
                         user: int = Depends(UserWrite.super_or_admin)):
    check_service_type: Service_type = await Service_type.objects.filter(
        name=new_service_type.name).all()
    if not check_service_type:
        new_service_type_obj = await Service_type(**new_service_type.dict()
                                                 ).save()
        return new_service_type_obj
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"service type with name:{new_service_type.name} already exist")


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[Service_typeOutput])
async def get_all_service_type(limit: Optional[int] = 10,
                               skip: Optional[int] = 0,
                               q: Optional[str] = ""):
    if q:
        all_service_type_obj: Service_type = await Service_type.objects.filter(
            ormar.and_(name__icontains=q)).limit(limit).offset(skip).all()
        return all_service_type_obj
    all_service_type_obj: Service_type = await Service_type.objects.limit(
        limit).offset(skip).all()
    if all_service_type_obj:
        return all_service_type_obj
    return []


@router.get(
    "/{service_type_id}",
    status_code=status.HTTP_200_OK,
    response_model=Service_typeOutput)
async def get_single_service(service_type_id: int):
    service_type_obj = await Service_type.objects.get_or_none(id=service_type_id
                                                             )
    if service_type_obj:
        return service_type_obj
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"service type with id: {service_type_id} is not found")


@router.put(
    "/{service_type_id}",
    status_code=status.HTTP_200_OK,
    response_model=Service_typeOutput)
async def update_service(service_type_id: int,
                         service_type_data: Service_typeInput,
                         user: int = Depends(UserWrite.super_or_admin)):
    service_type_obj: Service_type = await Service_type.objects.get_or_none(
        id=service_type_id)
    if not service_type_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"service type with id:{service_type_id} is not found")
    updated_service_type = await service_type_obj.update(
        **service_type_data.dict())
    return updated_service_type


@router.delete("/{service_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(service_type_id: int,
                         user: int = Depends(UserWrite.super_or_admin)):
    service_type_obj: Service_type = await Service_type.objects.get_or_none(
        id=service_type_id)
    if service_type_obj:
        await service_type_obj.delete()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="service is not found")
