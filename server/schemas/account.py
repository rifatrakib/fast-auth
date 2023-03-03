from datetime import datetime
from typing import Union

from pydantic import Field

from server.schemas.base import BaseSchemaAuthAPI, BaseSchemaORM
from server.schemas.token import JWTData


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


class UserInformationResponse(JWTData, BaseSchemaORM):
    is_active: bool = Field(
        default=False,
        title="active status",
        decription="Whether user is active, determined via email confirmation.",
    )
    is_verified: bool = Field(
        default=False,
        title="verification status",
        decription="Whether user is verified, determined via phone number verification.",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        title="time of insert",
        decription="Exact time when the user information was first saved.",
    )
    updated_at: Union[datetime, None] = Field(
        default=None,
        title="time of last update",
        decription="Exact time when the user information was last updated.",
    )
