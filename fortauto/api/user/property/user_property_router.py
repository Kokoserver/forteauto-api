from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fortauto.core.authentication import UserWrite
from fortauto.api.user.property import user_property_model
from fortauto.api.user.property import user_property_schema
from fortauto.api.user import user_model

router = APIRouter()


################################## user car detail #####################
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=user_property_schema.CarDetailResponse)
async def add_new_user_car(new_car_data: user_property_schema.CarDetail,
                           user:int = Depends(
                               UserWrite.current_user)):
    check_car = await user_property_model.Car.objects.get_or_none(
        vin_number=new_car_data.vin_number)
    if check_car:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"car with vin number {new_car_data.vin_number} already exist"
        )
    new_car_obj = user_property_model.Car(**new_car_data.dict(), owner=user)
    await new_car_obj.save()
    return new_car_obj


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[user_property_schema.CarDetailResponse])
async def all_ser_car(user:int = Depends(UserWrite.current_user)):
    all_user_cars_obj = await user_property_model.Car.objects.filter(owner=user
                                                                    ).all()
    if all_user_cars_obj:
        return all_user_cars_obj
    return []


@router.get(
    "/{car_id}",
    status_code=status.HTTP_200_OK,
    response_model=user_property_schema.CarDetailResponse)
async def get_single_user_car(car_id: int,
                              user:int = Depends(
                                  UserWrite.current_user)):
    car_obj = await user_property_model.Car.objects.get_or_none(
        id=car_id, owner=user)
    if car_obj:
        return car_obj
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"car with id: {car_id} doest not exists")


@router.put(
    "/{car_id}",
    status_code=status.HTTP_200_OK,
    response_model=user_property_schema.CarDetailResponse)
async def update_single_user_car(car_id: int,
                                 car_data: user_property_schema.CarDetail,
                                 user:int = Depends(
                                     UserWrite.current_user)):
    check_car_obj: user_property_model.Car = await user_property_model.Car.objects.get_or_none(
        id=car_id, owner=user)
    if check_car_obj:
        updated_car = await check_car_obj.update(**car_data.dict())
        return updated_car
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"car with vin number: {car_data.vin_number} or id: {car_id} does not exist"
    )


@router.delete("/{car_id}")
async def remove_single_user_car(car_id: int,
                                 user:int = Depends(
                                     UserWrite.current_user)):
    car_obj = await user_property_model.Car.objects.get_or_none(
        id=car_id, owner=user)
    if car_obj:
        await car_obj.delete()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"car with id: {car_id} doest not exists")
