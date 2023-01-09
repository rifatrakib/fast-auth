from datetime import datetime
from enum import Enum
from typing import Union

from pydantic import EmailStr, Field

from server.schemas.base import SchemaConfigBase
from server.utilities.converters import optional


class Gender(Enum):
    male = "m"
    female = "f"


class UserBase(SchemaConfigBase):
    username: str = Field(...)
    first_name: str = Field(...)
    middle_name: Union[str, None] = Field(None)
    last_name: Union[str, None] = Field(None)
    email: EmailStr = Field(...)
    phone_number: Union[str, None] = Field(None)
    gender: Union[Gender, None] = Field(None)
    birthday: Union[datetime, None] = Field(None)
    is_active: bool = Field(False)
    is_verified: bool = Field(False)
    is_logged_in: bool = Field(False)


class UserCreateRequest(UserBase):
    password: str = Field(...)


class UserCreate(UserBase):
    hashed_password: str = Field(...)


@optional
class UserUpdateRequest(UserCreateRequest):
    pass


class User(UserBase):
    id: int = Field(...)


class AccountWithToken(SchemaConfigBase):
    token: str
    username: str
    email: EmailStr
    is_verified: bool
    is_active: bool
    is_logged_in: bool
    created_at: datetime
    updated_at: Union[datetime, None]


class AccountInResponse(SchemaConfigBase):
    id: int
    details: AccountWithToken
