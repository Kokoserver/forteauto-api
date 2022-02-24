from datetime import datetime, timedelta
from fastapi import HTTPException, status
import jose
from jose import JWTError
from jose import jwt
import fortauto.conf.config as base_config


class JWTAUTH:

    @staticmethod
    def JwtEncoder(
            data: dict,
            duration: int = base_config.settings.access_token_expire_time):
        if duration:

            access_token_time = datetime.utcnow() + timedelta(
                minutes=int(duration))
            refresh_token_time = datetime.utcnow() + timedelta(
                days=int(base_config.settings.refresh_token_expire_time))
        data_access_token = {"data": data, "exp": access_token_time}
        data_refresh_token = {"data": data, "exp": refresh_token_time}
        try:
            encode_jwt_refresh = jwt.encode(
                claims=data_refresh_token,
                key=base_config.settings.refresh_key,
                algorithm=base_config.settings.jwt_algorithm,
            )
            encode_jwt_access = jwt.encode(
                claims=data_access_token,
                key=base_config.settings.secret_key,
                algorithm=base_config.settings.jwt_algorithm,
            )
            return encode_jwt_access, encode_jwt_refresh
        except jose.JWTError as e:
            raise HTTPException(
                detail={"error": "Error jwt error"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def DataEncoder(data: dict,
                    days: int = 0,
                    hours: int = 0,
                    minutes: int = 0,
                    seconds: int = 0,
                    secret_key: str = None):
        exp = None
        if days > 0:
            exp = datetime.utcnow() + timedelta(days=int(days))
        if hours > 0:
            exp = datetime.utcnow() + timedelta(hours=int(hours))
        if minutes > 0:
            exp = datetime.utcnow() + timedelta(minutes=int(minutes))
        if seconds > 0:
            exp = datetime.utcnow() + timedelta(seconds=int(seconds))

        if exp is not None: 
            data_to_encode = {"data":data, "exp":exp}
        else:
            data_to_encode = {"data": data}

        try:

            encoded_data = jwt.encode(
                claims=data_to_encode,
                key=secret_key if secret_key else
                base_config.settings.refresh_key,
                algorithm=base_config.settings.jwt_algorithm,
            )

            return encoded_data
        except JWTError as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Validation error",
            )

    @staticmethod
    def data_decoder(encoded_data: str, secret_key: str = None):
        try:
            payload = jwt.decode(
                token=encoded_data,
                key=secret_key if secret_key else
                base_config.settings.refresh_key,
                algorithms=base_config.settings.jwt_algorithm,
            )
            data: dict = payload.get("data")
            return False if not data else data
        except jose.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Validation error",
            )
