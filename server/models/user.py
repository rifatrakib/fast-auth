from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from sqlalchemy.sql import functions

from server.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    email = Column(String(256), unique=True, index=True, nullable=False)
    hashed_password = Column(String(1024), nullable=True)
    hash_salt = Column(String(1024), nullable=True)
    phone_number = Column(String(16), unique=True, index=True, nullable=True)
    is_active = Column(Boolean, nullable=False, default=False, index=True)
    is_verified = Column(Boolean, nullable=False, default=False, index=True)
    is_logged_in = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=functions.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=True,
        server_onupdate=FetchedValue(for_update=True),
    )

    user = relationship("User", back_populates="account", uselist=False)
    validator = relationship("AccountValidation", back_populates="account", uselist=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(
        Integer,
        ForeignKey("accounts.id"),
        index=True,
        unique=True,
        nullable=False,
    )
    first_name = Column(String(64), nullable=False)
    middle_name = Column(String(256), default=None, nullable=True)
    last_name = Column(String(64), nullable=False)
    gender = Column(String(1), default=None, nullable=True)
    birthday = Column(DateTime(timezone=True), default=None, nullable=True)

    account = relationship(
        "Account",
        back_populates="user",
        cascade="all, delete-orphan",
        single_parent=True,
    )


class AccountValidation(Base):
    __tablename__ = "account_validations"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(
        Integer,
        ForeignKey("accounts.id"),
        index=True,
        unique=True,
        nullable=False,
    )
    validation_key = Column(String(64), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=functions.now(),
    )

    account = relationship(
        "Account",
        back_populates="validator",
        cascade="all, delete-orphan",
        single_parent=True,
    )
