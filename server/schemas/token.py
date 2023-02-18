from datetime import datetime
from typing import Union

from pydantic import EmailStr

from server.schemas.base import BaseSchemaAPI


class JWTData(BaseSchemaAPI):
    id: int
    username: str
    email: EmailStr
    phone_number: Union[str, None] = None


class JWToken(BaseSchemaAPI):
    exp: datetime
    sub: str
