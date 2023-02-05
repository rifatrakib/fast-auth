from datetime import datetime
from typing import Union

from pydantic import EmailStr

from server.schemas.base import BaseSchemaAPI


class AccountPostRequestSchema(BaseSchemaAPI):
    username: str
    password: str


class SignupRequestSchema(AccountPostRequestSchema):
    email: EmailStr
    phone_number: Union[str, None] = None


class LoginRequestSchema(AccountPostRequestSchema):
    pass


class JWTData(BaseSchemaAPI):
    id: int
    username: str
    email: str


class JWToken(BaseSchemaAPI):
    exp: datetime
    sub: str
