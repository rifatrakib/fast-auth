from datetime import datetime, timedelta
from typing import Union

from jose import JWTError, jwt
from pydantic import ValidationError

from server.configurations.core import settings
from server.models.user import Account
from server.schemas.token import JWTData, JWToken
from server.utilities.exceptions import EntityDoesNotExist


class JWTGenerator:
    def __init__(self):
        pass

    def _generate_jwt_token(
        self,
        *,
        token_data: dict[str, str],
        expires_delta: Union[timedelta, None] = None,
    ) -> str:
        to_encode = token_data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.JWT_MIN)

        to_encode.update(JWToken(exp=expire, sub=settings.JWT_SUBJECT).dict())
        return jwt.encode(
            to_encode,
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    def generate_access_token(self, account: Account) -> str:
        if not account:
            raise EntityDoesNotExist("cannot generate JWT token for without Account entity!")

        return self._generate_jwt_token(
            jwt_data=JWTData(username=account.username, email=account.email).dict(),
            expires_delta=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRATION_TIME),
        )

    def retrieve_details_from_token(self, token: str, secret_key: str) -> JWTData:
        try:
            payload = jwt.decode(token=token, key=secret_key, algorithms=[settings.JWT_ALGORITHM])
            jwt_data = JWTData(username=payload["username"], email=payload["email"])
            return jwt_data
        except JWTError as token_decode_error:
            raise ValueError("unable to decode JWT Token") from token_decode_error
        except ValidationError() as validation_error:
            raise ValueError("invalid payload in token") from validation_error


def get_jwt_generator() -> JWTGenerator:
    return JWTGenerator()


jwt_generator: JWTGenerator = get_jwt_generator()
