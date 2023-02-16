from datetime import datetime, timedelta
from typing import Dict, Union

from jose import JWTError, jwt
from pydantic import ValidationError

from server.core.config import settings
from server.models.user import Account
from server.schemas.token import JWTData, JWToken
from server.services.exceptions import EntityDoesNotExist


class JWTGenerator:
    def _generate_jwt(
        self,
        *,
        data: Dict[str, str],
        expires_delta: Union[datetime, None] = None,
    ) -> str:
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.JWT_MIN)

        to_encode.update(JWToken(exp=expire, sub=settings.JWT_SUBJECT).dict())
        return jwt.encode(to_encode, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    def generate_access_token(self, account: Account) -> str:
        if not account:
            raise EntityDoesNotExist("cannot generate JWT for without Account entity!")

        return self._generate_jwt(
            data=JWTData(
                id=account.id,
                username=account.username,
                email=account.email,
                phone_number=account.phone_number,
            ).dict(),
            expires_delta=timedelta(minutes=settings.JWT_MIN),
        )

    def retrieve_token_details(self, token: str) -> JWTData:
        try:
            payload = jwt.decode(
                token=token,
                key=settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            jwt_data = JWTData(
                id=payload["id"],
                username=payload["username"],
                email=payload["email"],
                phone_number=payload["phone_number"],
            )
        except JWTError as token_decode_error:
            raise ValueError("unable to decode JWT") from token_decode_error
        except ValidationError as validation_error:
            raise ValueError("invalid payload in JWT") from validation_error
        return jwt_data


def get_jwt_generator() -> JWTGenerator:
    return JWTGenerator()


jwt_generator: JWTGenerator = get_jwt_generator()
