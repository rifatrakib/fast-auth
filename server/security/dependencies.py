from typing import Callable, Type

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from server.database import get_session
from server.schemas.token import JWTData
from server.security.token import jwt_generator
from server.sql.base import SQLBase

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
