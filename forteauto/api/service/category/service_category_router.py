from typing import List
from fastapi import APIRouter, Depends, Response, status, HTTPException
from core.authentication import UserWrite
from api.service.category.service_category_model import ServiceCategory
from api.service.category.service_category_schema import ServiceCategoryInput, ServiceCategoryOutput


category_router = APIRouter()


@category_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ServiceCategoryOutput)
async def create_service(new_service_category: ServiceCategoryInput,
                         user:int = Depends(UserWrite.is_admin)):
    check_service_category = await ServiceCategory.objects.filter(
        name=new_service_category.name).first()
    if not check_service_category:
        new_service_category_obj = await ServiceCategory(
            **new_service_category.dict()).save()
        return new_service_category_obj
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Service category category already exists")


@category_router.put(
    "/{service_category_id}",
    status_code=status.HTTP_200_OK,
    response_model=ServiceCategoryOutput)
async def update_service(service_category_id: int,
                         service_category_data: ServiceCategoryInput,
                         user:int = Depends(UserWrite.is_admin)):
    check_service_category_name_exist: ServiceCategory = await ServiceCategory.objects.filter(
        id=service_category_id).first()
    if check_service_category_name_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service category with id: {service_category_id} does not exist"
        )

    check_service_category: ServiceCategory = await ServiceCategory.objects.filter(
        name=service_category_data.name).first()
    if check_service_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Service category with name: {service_category_data.name} already exist"
        )

    updated_service_category_obj: ServiceCategory = await check_service_category.update(
        **service_category_data.dict())
    return updated_service_category_obj


@category_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[ServiceCategoryOutput])
async def get_service_type_list():
    service_categories = await ServiceCategory.objects.all()
    if service_categories:
        return service_categories
    return []


@category_router.get(
    "/{service_category_Id}",
    status_code=status.HTTP_200_OK,
    response_model=ServiceCategoryOutput)
async def get_single_service(service_category_Id: int):
    service_category_obj = await ServiceCategory.objects.filter(
        id=service_category_Id)
    if service_category_obj:
        return service_category_obj
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Service category not found")


@category_router.delete(
    "/{service_category_Id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(service_category_Id: str,
                         user:int = Depends(UserWrite.is_admin)):
    deleted_to_category: ServiceCategory = await ServiceCategory.objects.filter(
        id=service_category_Id).first()
    if deleted_to_category:
        await deleted_to_category.delete()
        return Response(status_code=status.HTTP_200_OK)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Service category not found")
