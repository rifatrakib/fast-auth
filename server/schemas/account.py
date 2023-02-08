from typing import Union

from pydantic import EmailStr

from server.schemas.base import BaseSchemaAPI
from server.schemas.token import AccountToken


class AccountPostRequestSchema(BaseSchemaAPI):
    username: str
    password: str


class SignupRequestSchema(AccountPostRequestSchema):
    email: EmailStr
    phone_number: Union[str, None] = None


class SignupResponseSchema(BaseSchemaAPI):
    id: int
    authentication_token: AccountToken


class LoginRequestSchema(AccountPostRequestSchema):
    pass
