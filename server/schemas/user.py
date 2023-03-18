from datetime import datetime
from typing import Union

from server.schemas.base import BaseSchemaAPI
from server.services.validators import Gender


class UserResponseSchema(BaseSchemaAPI):
    first_name: str
    middle_name: Union[str, None] = None
    last_name: str
    gender: Union[Gender, None] = None
    birthday: Union[datetime, None] = None


class UserUpdateSchema(BaseSchemaAPI):
    first_name: Union[str, None] = None
    middle_name: Union[str, None] = None
    last_name: Union[str, None] = None
    gender: Union[Gender, None] = None
    birthday: Union[datetime, None] = None
