from pydantic import Field

from server.schemas.base import BaseSchemaAuthAPI


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
