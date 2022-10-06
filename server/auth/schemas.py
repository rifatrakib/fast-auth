import json
import re
from datetime import datetime
from enum import Enum
from typing import Union

from pydantic import BaseModel, EmailStr, validator


class Gender(Enum):
    male = "m"
    female = "f"


class UserBase(BaseModel):
    username: str
    first_name: str
    middle_name: Union[str, None] = None
    last_name: Union[str, None] = None
    email_address: EmailStr
    phone_number: Union[str, None] = None
    gender: Union[Gender, None] = None
    birthday: Union[datetime, None] = None
    is_active: bool

    @validator("phone_number")
    def phone_number_validation(cls, value):
        regex = r"^([0-9\(\)\/\+ \-]*)$"
        pat = re.compile(regex)
        if value and not re.search(pat, value):
            raise ValueError("phone number invalid")

        return value


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Password(BaseModel):
    password: str

    @validator("password")
    def password_validator(cls, value):
        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])([A-Za-z\d@$!%*#?&]{6,32}$"
        pat = re.compile(regex)
        invalid_message = {
            "message": "password must have the following fields",
            "uppercase letters": 1,
            "lowercase letters": 1,
            "special characters (@$!%*#?&)": 1,
            "length": {"min": 6, "max": 32},
        }
        if not value:
            raise ValueError("no password provided")
        elif not re.search(pat, value):
            raise ValueError(json.dumps(invalid_message))

        return value


class AuthToken(BaseModel):
    access_token: str
    token_type: str


class Payload(BaseModel):
    username: str
