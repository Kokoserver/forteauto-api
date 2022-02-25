from re import U
from fastapi import (APIRouter, Depends, Response, status, HTTPException,
                     BackgroundTasks)
from forteauto.core import password
from forteauto.core.mail import mailer
from forteauto.core import authentication as auths
from forteauto.core import jwt_anth
from forteauto.conf import config
import forteauto.api.api_base_schema as base_schema
from forteauto.api.user import user_model
from forteauto.api.user import user_schema

router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=base_schema.Message)
async def user_regsiter(
        new_user_data: user_schema.UserRegisterInput,
        background_task: BackgroundTasks) -> base_schema.Message:
    check_user: user_model.User = await user_model.User.objects.get_or_none(
        email=new_user_data.email)
    if check_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account already exist")
    new_user: user_model.User = user_model.User(**new_user_data.dict())
    new_user.hash_password()
    await new_user.save()
    if new_user:
        token = jwt_anth.JWTAUTH.DataEncoder(data={"id": new_user.id})
        mail_template_context = {
            "url":
                f"{config.settings.frontend_url}/user/{token}/confirmation",
            "button_label":
                "confirm",
            "title":
                "user email confirmation link",
            "description":
                f"Welcome to <b>{config.settings.website_name}</b>, kindly click on the link below to activate your account",
        }
        new_mail = mailer.Mailer(
            website_name=config.settings.website_name,
            template_name="action.html",
            subject="Email confirmation",
            context=mail_template_context)
        background_task.add_task(new_mail.send_mail, email=[new_user.email])
        return base_schema.Message(
            message="Account was created successfully, an email confirmation link has been to your mail"
        )


@router.post(
    "/activate",
    status_code=status.HTTP_200_OK,
    response_model=base_schema.Message)
async def verify_user_email(
        user_token: user_schema.UserAccountVerifyToken) -> base_schema.Message:
    data: dict = jwt_anth.JWTAUTH.data_decoder(encoded_data=user_token.token)

    if data:
        user_obj: user_model.User = await user_model.User.objects.get_or_none(
            id=data.get("id", None))
        if user_obj and user_obj.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Acount has been already activated")
        if user_obj:
            await user_obj.update(is_active=True)
            return base_schema.Message(
                message="Account was activated successfuly")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account does not exist")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid token was provided")


@router.post(
    "/password",
    status_code=status.HTTP_200_OK,
    response_model=base_schema.Message)
async def reset_password_link(background_task: BackgroundTasks,
                              user_data: user_schema.GetPasswordResetLink):
    user_obj: user_model.User = await user_model.User.objects.get_or_none(
        email=user_data.email)
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account does not exist")
    if user_obj:
        token = jwt_anth.JWTAUTH.DataEncoder(data={"id": user_obj.id}, days=1)
        mail_template_context = {
            "url":
                f"{config.settings.frontend_url}/user/{token}/password_reset",
            "button_label":
                "reset password",
            "title":
                "password reset link",
            "description":
                "You resquest for password reset link, if not you please ccontact admin",
        }
        new_mail = mailer.Mailer(
            website_name=config.settings.website_name,
            template_name="action.html",
            context=mail_template_context,
            subject="Password reset link",
        )
        background_task.add_task(new_mail.send_mail, email=[user_obj.email])
        return base_schema.Message(
            message="password reset token has been sent to youe email, link expire after 24 hours"
        )


@router.put(
    "/password",
    status_code=status.HTTP_200_OK,
    response_model=base_schema.Message)
async def update_user_password(
        user_data: user_schema.PasswordResetInput) -> base_schema.Message:
    token_data: dict = jwt_anth.JWTAUTH.data_decoder(
        encoded_data=user_data.token)
    if token_data:
        user_obj: user_model.User = await user_model.User.objects.get_or_none(
            id=token_data.get("id", None))
        if user_obj:
            new_password: bytes = password.Hasher.hash_password(
                user_data.password)
            await user_obj.update(password=new_password)
            return base_schema.Message(
                message="password was reset successfully")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token was provided",
        )


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=user_schema.UserDataOut)
async def current_user_data(user: int = Depends(
    auths.UserWrite.current_user)) -> user_schema.UserDataOut:
    user_data = await user_model.User.objects.get_or_none(id=user)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does nnot exist")
    return user_data.dict()


# @router.get(
#     "/details",
#     status_code=status.HTTP_200_OK,
#     response_model=user_model.User,
#     response_model_exclude={"password"})
# def get_all_current_user_data(user_data:int = Depends(
#     auths.UserWrite.is_admin)) -> user_model.User:
#     return user_data


@router.delete(
    "/{userId}/remove",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model_exclude={"password"},
)
async def remove_user_data(
    userId: int, admin: int = Depends(auths.UserWrite.super_or_admin)) -> None:
    user_to_remove = await user_model.User.objects.get_or_none(id=userId)
    if user_to_remove:
        await user_to_remove.delete()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with {userId} does not exist",
    )
