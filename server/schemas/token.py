from datetime import datetime
from typing import Union

from pydantic import EmailStr

from server.schemas.base import BaseSchemaAPI


class AccountToken(BaseSchemaAPI):
    token: str
    username: str
    email: EmailStr
    phone_number: Union[str, None] = None
    is_verified: bool
    is_active: bool
    is_logged_in: bool
    created_at: datetime
    updated_at: Union[datetime, None] = None


class JWTData(BaseSchemaAPI):
    id: int
    username: str
    email: str


class JWToken(BaseSchemaAPI):
    exp: datetime
    sub: str
