from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def create_new_user(session: AsyncSession, user: schemas.UserCreate):
    data = user.dict()
    data["gender"] = data["gender"].value
    user_data = models.User(**data)
    session.add(user_data)
    await session.commit()
    return user_data


async def get_user_by_id(session: AsyncSession, user_id: int):
    query = select(models.User).filter(models.User.id == user_id)
    user_data = await session.execute(query)
    user = user_data.scalars().first()
    return user


async def get_user_by_username(session: AsyncSession, username: str):
    query = select(models.User).filter(models.User.username == username)
    user_data = await session.execute(query)
    user = user_data.scalars().first().__dict__
    return user


async def get_user_by_email(session: AsyncSession, email_address: str):
    query = select(models.User).filter(models.User.email_address == email_address)
    user_data = await session.execute(query)
    user = user_data.scalars().first().__dict__
    return user
