from datetime import datetime
from typing import Union

from pydantic import EmailStr

from server.schemas.base import BaseSchemaAPI


class SignupRequestSchema(BaseSchemaAPI):
    username: str
    email: EmailStr
    password: str
    phone_number: Union[str, None] = None


class JWTData(BaseSchemaAPI):
    id: int
    username: str
    email: str


class JWToken(BaseSchemaAPI):
    exp: datetime
    sub: str
