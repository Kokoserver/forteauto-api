from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fortauto.api.user.address import user_address_model
from fortauto.api.user.address import user_address_schema
from fortauto.api.user import user_model
from fortauto.core.authentication import UserWrite

router = APIRouter()

################################## user address detail #####################


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=user_address_schema.AddressDetailsResponse)
async def add_new_user_address(
    new_address_data: user_address_schema.AddressDetails,
    user: int = Depends(UserWrite.current_user)):
    check_address = await user_address_model.Address.objects.get_or_none(
        city=new_address_data.city,
        state=new_address_data.state,
        address=new_address_data.address,
        owner=user)
    if not check_address:
        new_address_obj = user_address_model.Address(
            **new_address_data.dict(), owner=user)
        await new_address_obj.save()
        return new_address_obj
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"address already exist")


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[user_address_schema.AddressDetailsResponse])
async def all_ser_address(user: int = Depends(UserWrite.current_user)):
    all_user_addresss_obj = await user_address_model.Address.objects.filter(
        owner=user).all()
    if all_user_addresss_obj:
        return all_user_addresss_obj
    return []
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No address was found")


@router.get(
    "/{address_id}",
    status_code=status.HTTP_200_OK,
    response_model=user_address_schema.AddressDetailsResponse)
async def get_single_user_address(address_id: int,
                                  user: int = Depends(UserWrite.current_user)):
    address_obj = await user_address_model.Address.objects.get_or_none(
        id=address_id, owner=user)
    if address_obj:
        return address_obj
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"address with id: {address_id} doest not exists")


@router.put(
    "/{address_id}",
    status_code=status.HTTP_200_OK,
    response_model=user_address_schema.AddressDetailsResponse)
async def update_single_user_address(
    address_id: int,
    address_data: user_address_schema.AddressDetails,
    user: int = Depends(UserWrite.current_user)):
    check_address_obj: user_address_model.Address = await user_address_model.Address.objects.get_or_none(
        id=address_id, owner=user)
    if check_address_obj:
        updated_address = await check_address_obj.update(**address_data.dict())
        return updated_address
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"address does not exist")


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_single_user_address(address_id: int,
                                     user: int = Depends(
                                         UserWrite.current_user)):
    address_obj = await user_address_model.Address.objects.get_or_none(
        id=address_id, owner=user)
    if address_obj:
        await address_obj.delete()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"address with id: {address_id} doest not exists")
