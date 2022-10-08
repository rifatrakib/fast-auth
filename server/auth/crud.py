from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def create_new_user(session: AsyncSession, user: schemas.UserCreate):
    data = user.dict()
    data["gender"] = data["gender"].value
    query = insert(models.User).values(data).returning(models.User.id)
    user_id = await session.execute(query)
    await session.commit()
    user_data = {**data, "id": user_id.scalars().first()}
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
