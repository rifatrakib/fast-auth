from typing import Union

from pydantic import EmailStr

from server.schemas.base import BaseSchemaAPI, BaseSchemaAuthAPI


class AccountPostRequestSchema(BaseSchemaAPI):
    username: str
    password: str


class SignupRequestSchema(AccountPostRequestSchema):
    email: EmailStr
    phone_number: Union[str, None] = None


class MessageResponseSchema(BaseSchemaAuthAPI):
    msg: str


class AuthResponseSchema(BaseSchemaAuthAPI):
    token_type: str
    access_token: str


class LoginRequestSchema(AccountPostRequestSchema):
    pass
