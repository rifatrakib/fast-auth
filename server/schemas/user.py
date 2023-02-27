from datetime import datetime
from typing import Union

from pydantic import Field

from server.schemas.base import BaseSchemaAPI, BaseSchemaORM
from server.schemas.token import JWTData


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


class UpdateUserPassword(BaseSchemaAPI):
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
