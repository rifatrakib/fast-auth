from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from server.core.config import settings


def get_database_url():
    username = settings.DB_USERNAME
    password = settings.DB_PASSWORD
    host = settings.DB_HOST
    port = settings.DB_PORT
    database_name = settings.DATABASE_NAME
    url = f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database_name}"
    return url


def get_database_session():
    url = get_database_url()
    engine = create_async_engine(url)
    SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    return SessionLocal


async def get_session():
    try:
        session: AsyncSession = get_database_session()()
        yield session
    finally:
        await session.close()


Base = declarative_base()
