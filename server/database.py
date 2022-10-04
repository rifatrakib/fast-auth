import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_url():
    user = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    server = os.environ.get("DB_HOST") + ":" + os.environ.get("DB_PORT")
    db = os.environ.get("DATABASE_NAME")
    return f"postgresql://{user}:{password}@{server}/{db}"


SQLALCHEMY_DATABASE_URL = get_url()
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
