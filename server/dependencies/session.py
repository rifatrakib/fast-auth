from typing import Callable, Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from server.crud.base import CRUD
from server.database import get_session


def get_async_session(session_type: Type[CRUD]) -> Callable[[AsyncSession], CRUD]:
    def _get_async_session(async_session: AsyncSession = Depends(get_session)) -> CRUD:
        return session_type(async_session=async_session)

    return _get_async_session
