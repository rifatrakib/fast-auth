from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from server.utils import get_url


def get_database_session():
    url = get_url()
    engine = create_async_engine(url)
    SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    return SessionLocal


async def get_session():
    try:
        session: AsyncSession = get_database_session()()
        yield session
    except Exception as e:
        print(e)
        await session.rollback()
    finally:
        await session.close()


Base = declarative_base()
