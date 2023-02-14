from typing import Callable, Type

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from server.database import get_session
from server.schemas.token import JWTData
from server.security.token import jwt_generator
from server.services.exceptions import EntityDoesNotExist
from server.sql.base import SQLBase
from server.sql.user import AccountCRUD

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")


def generate_crud_instance(name: Type[SQLBase]) -> Callable[[], SQLBase]:
    def _create_crud_instance(
        session: AsyncSession = Depends(get_session),
    ) -> SQLBase:
        return name(session=session)

    return _create_crud_instance


async def decode_user_token(
    token: str = Depends(oauth2_scheme),
):
    try:
        user_data: JWTData = jwt_generator.retrieve_token_details(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"msg": "could not validate credentials"},
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_data


async def get_current_user(
    user_data: JWTData = Depends(decode_user_token),
    account: AccountCRUD = Depends(generate_crud_instance(name=AccountCRUD)),
):
    try:
        user = await account.read_account_by_username(user_data.username)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"msg": "could not validate credentials"},
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
