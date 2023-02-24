from datetime import datetime
from typing import Union

from pydantic import EmailStr, Field

from server.schemas.base import BaseSchemaAPI


class JWTData(BaseSchemaAPI):
    id: int = Field(
        title="user ID",
        decription="Unique ID that can be used to distinguish between users.",
    )
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
    email: EmailStr = Field(
        title="email",
        decription="Unique email that can be used for account activation.",
    )
    phone_number: Union[str, None] = Field(
        default=None,
        title="phone number",
        decription="Unique phone number that can be used for account verification.",
    )


class JWToken(BaseSchemaAPI):
    exp: datetime = Field(
        title="expiry of token",
        decription="A timestamp definining tokens period of validity.",
    )
    sub: str = Field(
        title="OAuth2.0 token subject",
        decription="A string for subject of the token as per OAuth2.0 requirements.",
    )
