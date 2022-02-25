from fastapi import APIRouter, Depends, status, HTTPException
from api.user import user_model
from api.user.auth import user_auth_schema
from core import jwt_anth
from core import authentication

router = APIRouter()


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=user_auth_schema.TokenData)
async def auth_login(
        auth_data: authentication.OAuth2PasswordRequestForm = Depends()
) -> user_auth_schema.TokenData:
    check_user: user_model.User = await user_model.User.objects.get_or_none(
        email=auth_data.username)
    if not check_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="incorrect email or password")
    check_password = check_user.check_password(auth_data.password)
    if not check_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect email or password")
    if check_user.is_active:
        get_jwt_data_for_encode = user_auth_schema.ToEncode(**check_user.dict())
        access_token, refresh_token = jwt_anth.JWTAUTH.JwtEncoder(
            data=get_jwt_data_for_encode.dict())
        return user_auth_schema.TokenData(
            access_token=access_token, refresh_token=refresh_token)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="you are yet to verify you account, please check your email",
    )


@router.post(
    "/token_refresh",
    status_code=status.HTTP_200_OK,
    response_model=user_auth_schema.TokenData)
async def auth_login_token_refresh(
    user_token: user_auth_schema.UserRefreshTokenInput
) -> user_auth_schema.TokenData:

    token_data = jwt_anth.JWTAUTH.data_decoder(
        encoded_data=user_token.refresh_token)
    check_user: user_model.User = await user_model.User.objects.get_or_none(
        id=token_data.get("id", None))
    if not check_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account doe not exist",
        )
    access_token, refresh_token = jwt_anth.JWTAUTH.JwtEncoder(
        data={"id": check_user.id})
    return user_auth_schema.TokenData(
        access_token=access_token, refresh_token=refresh_token)
