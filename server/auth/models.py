import re
from datetime import datetime, timezone

from email_validator import EmailNotValidError, validate_email
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import validates

from server.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, default=None)
    last_name = Column(String, default=None)
    email_address = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone_number = Column(String, unique=True, index=True)
    gender = Column(String, default=None)
    birthday = Column(DateTime(timezone=True), default=None)
    is_active = Column(Boolean, default=True)

    @validates("email_address")
    def email_validator(self, key, address):
        try:
            val = validate_email(address)
            email = val["email"]
            return email
        except EmailNotValidError as e:
            print(str(e))
            print(f"provide a valid {key}")

    @validates("phone_number")
    def phone_number_validator(self, key, number):
        regex = r"^([0-9\(\)\/\+ \-]*)$"
        pat = re.compile(regex)
        if number and not re.search(pat, number):
            raise ValueError("phone number invalid")

        return number

    @validates("birthday")
    def birthday_validator(self, key, dt):
        if dt > datetime.now().replace(tzinfo=timezone.utc):
            raise ValueError(f"birthday cannot be a future date. provide a valid {key}")

        return dt
