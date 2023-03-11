from datetime import datetime
from typing import Callable, Type, Union

import aioredis
from aioredis.client import Redis
from fastapi import Depends, Form
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from server.cache.base import RedisBase
from server.core.config import settings
from server.database import get_session
from server.models.user import Account
from server.schemas.token import JWTData
from server.security.token import jwt_generator
from server.services.exceptions import EntityDoesNotExist
from server.services.messages import (
    http_exc_400_inactive_user,
    http_exc_400_unverified_user,
    http_exc_403_credentials_exception,
    http_exc_412_password_mismatch,
    http_exc_422_field_required,
)
from server.services.validators import Gender
from server.sql.base import SQLBase
from server.sql.user import AccountCRUD

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/signin")


def generate_crud_instance(name: Type[SQLBase]) -> Callable[[], SQLBase]:
    def _create_crud_instance(
        session: AsyncSession = Depends(get_session),
    ) -> Type[SQLBase]:
        return name(session=session)

    return _create_crud_instance


async def get_redis_client() -> Redis:
    try:
        redis = await aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        yield redis
    finally:
        await redis.close()


def generate_redis_client(name: Type[RedisBase]) -> Callable[[], RedisBase]:
    def _create_redis_client(
        redis: Redis = Depends(get_redis_client),
    ) -> RedisBase:
        return name(redis=redis)

    return _create_redis_client


async def decode_user_token(
    token: str = Depends(oauth2_scheme),
) -> JWTData:
    try:
        user_data: JWTData = jwt_generator.retrieve_token_details(token)
    except ValueError:
        raise await http_exc_403_credentials_exception()
    return user_data


async def get_current_user(
    user_data: JWTData = Depends(decode_user_token),
    account: AccountCRUD = Depends(generate_crud_instance(name=AccountCRUD)),
):
    try:
        user = await account.read_account_by_username(user_data.username)
    except EntityDoesNotExist:
        raise await http_exc_403_credentials_exception()
    return user


async def get_current_active_user(
    user: Account = Depends(get_current_user),
):
    if not user.is_active:
        raise await http_exc_400_inactive_user()
    return user


async def get_current_verified_user(
    user: Account = Depends(get_current_user),
):
    if not user.is_verified:
        raise await http_exc_400_unverified_user()
    return user


def username_form_field(
    username: str = Form(
        title="username",
        decription="""
            Unique username containing letters, numbers, and
            any of (., _, -, @) in between 6 to 32 characters.
        """,
        regex=r"^[\w.@_-]{6,32}$",
        min_length=6,
        max_length=32,
    ),
):
    return username


def email_form_field(
    email: EmailStr = Form(
        title="email",
        decription="Unique email that can be used for account activation.",
    ),
):
    return email


def phone_number_form_field(
    phone_number: Union[str, None] = Form(
        default=None,
        title="phone number",
        decription="Unique phone number that can be used for account verification.",
    ),
):
    return phone_number


def password_form_field(
    password: str = Form(
        alias="newPassword",
        title="new password",
        decription="""
            Password containing at least 1 uppercase letter, 1 lowercase letter,
            1 number, 1 character that is neither letter nor number, and
            between 8 to 32 characters.
        """,
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,64}$",
        min_length=8,
        max_length=64,
    ),
):
    return password


async def new_password_form(
    new_password: str = Form(
        alias="newPassword",
        title="new password",
        decription="""
            Password containing at least 1 uppercase letter, 1 lowercase letter,
            1 number, 1 character that is neither letter nor number, and
            between 8 to 32 characters.
        """,
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,64}$",
        min_length=8,
        max_length=64,
    ),
    repeat_new_password: str = Form(
        alias="repeatNewPassword",
        title="repeat new password",
        decription="Type the same pasword again.",
    ),
):
    if new_password != repeat_new_password:
        raise await http_exc_412_password_mismatch()
    return new_password


def first_name_form_field(optional: bool):
    async def _first_name_form_field(
        first_name: Union[str, None] = Form(
            default=None,
            alias="firstName",
            title="First Name",
            description="First Name of the user",
        ),
    ):
        if not optional and not first_name:
            raise await http_exc_422_field_required("first_name")
        return first_name

    return _first_name_form_field


async def middle_name_form_field(
    middle_name: Union[str, None] = Form(
        default=None,
        alias="middleName",
        title="Middle Name",
        description="Middle Name of the user",
    ),
):
    return middle_name


def last_name_form_field(optional: bool):
    async def _last_name_form_field(
        last_name: Union[str, None] = Form(
            default=None,
            alias="lastName",
            title="Last Name",
            description="Last Name of the user",
        ),
    ):
        if not optional and not last_name:
            raise await http_exc_422_field_required("last_name")
        return last_name

    return _last_name_form_field


def gender_form_field(
    gender: Union[Gender, None] = Form(
        default=None,
        alias="gender",
        title="Gender",
        description="Gender of the user",
    ),
):
    return gender


def birthday_form_field(
    birthday: Union[datetime, None] = Form(
        default=None,
        alias="birthday",
        title="Birthday",
        description="Birthday of the user",
    ),
):
    return birthday
