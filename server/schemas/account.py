from typing import Union

from pydantic import EmailStr, Field

from server.schemas.base import BaseSchemaAPI, BaseSchemaAuthAPI


class AccountPostRequestSchema(BaseSchemaAPI):
    username: str = Field(
        title="username",
        decription="""
            Unique username containing letters, numbers, and
            any of (., _, -, @) in between 6 to 32 characters.
        """,
        regex=r"^[\w.@_-]{6,32}$",
        min_length=6,
        max_length=32,
    )
    password: str = Field(
        title="password",
        decription="""
            Password containing at least 1 uppercase letter, 1 lowercase letter,
            1 number, 1 character that is neither letter nor number, and
            between 8 to 32 characters.
        """,
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,64}$",
        min_length=8,
        max_length=64,
    )


class SignupRequestSchema(AccountPostRequestSchema):
    email: EmailStr = Field(
        title="email",
        decription="Unique email that can be used for account activation.",
    )
    phone_number: Union[str, None] = Field(
        default=None,
        title="phone number",
        decription="Unique phone number that can be used for account verification.",
    )


class MessageResponseSchema(BaseSchemaAuthAPI):
    msg: str = Field(
        title="message",
        decription="Short message explaining reason of failure.",
    )


class AuthResponseSchema(BaseSchemaAuthAPI):
    token_type: str = Field(
        title="OAuth2.0 token type",
        decription="A string for token type as per OAuth2.0 requirements.",
    )
    access_token: str = Field(
        title="access token",
        decription="Access token prepared from user data having expiry.",
    )


class LoginRequestSchema(AccountPostRequestSchema):
    pass
