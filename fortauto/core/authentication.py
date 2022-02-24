from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jose
import fortauto.conf.config as base_config
from fortauto.api.user import user_model

Oauth_schema = OAuth2PasswordBearer(
    tokenUrl=f"{base_config.settings.api_url}/auth/login")


class UserAuth:

    @staticmethod
    async def authenticate(token: str = Depends(Oauth_schema)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload:dict = jose.jwt.decode(
                token=token,
                key=base_config.settings.secret_key,
                algorithms=[base_config.settings.jwt_algorithm],
            )
            user: dict = payload.get("data", None)
            
            if user is None:
                raise credentials_exception
            if not user.get("id", None) and not user.get("role", None):
                raise credentials_exception
            return user
        except jose.JWTError:
            raise credentials_exception


class UserWrite:

    @staticmethod
    def is_admin(user:dict = Depends(UserAuth.authenticate)):
        if user.get("role") == user_model.UserRole.admin:
            return user.get("id")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin can perform this operation",
        )

    @staticmethod
    def is_supper_admin(user:dict = Depends(UserAuth.authenticate)):
        if user.get("role") == user_model.UserRole.super_admin:
            return user.get("id")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only super admin can perform this operation",
        )
    @staticmethod
    def super_or_admin(user:dict = Depends(UserAuth.authenticate)):
        if user.get("role") == user_model.UserRole.super_admin or user.get("role") == user_model.UserRole.admin:
            return user.get("id")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only super admin can perform this operation",
        )

    @staticmethod
    def current_user(user:dict = Depends(UserAuth.authenticate)):
        if user.get("is_active", None):
            return user.get("id", False)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is not active")
