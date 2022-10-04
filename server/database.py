from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from server.utils import get_url


async def get_database_session():
    url = get_url()
    engine = create_async_engine(url, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    return SessionLocal


Base = declarative_base()
