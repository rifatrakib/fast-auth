import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from .utils import get_url

SQLALCHEMY_DATABASE_URL = get_url()
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = databases.Database(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()
