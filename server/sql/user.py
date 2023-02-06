from typing import Sequence

from sqlalchemy import select

from server.models.user import Account
from server.schemas.user import LoginRequestSchema, SignupRequestSchema
from server.security.password import pwd_generator
from server.services.exceptions import (
    EntityAlreadyExists,
    EntityDoesNotExist,
    PasswordDoesNotMatch,
)
from server.sql.base import SQLBase


class AccountCRUD(SQLBase):
    async def create_account(self, data: SignupRequestSchema) -> Account:
        new_account = Account(**data.dict(), is_logged_in=True)
        new_account.hash_salt = pwd_generator.generate_salt
        new_account.hashed_password = pwd_generator.generate_hashed_password(
            hash_salt=new_account.hash_salt,
            password=data.password,
        )

        self.session.add(new_account)
        await self.session.commit()
        await self.session.refresh(instance=new_account)
        return new_account

    async def read_accounts(self, page: int = 1, page_size: int = 10) -> Sequence[Account]:
        stmt = select(Account).offset((page - 1) * page_size).limit(page_size)
        query = await self.session.execute(statement=stmt)
        return query.scalars().all()

    async def read_account_by_id(self, id: int) -> Account:
        stmt = select(Account).where(Account.id == id)
        query = await self.session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist(f"account with id `{id}` does not exist!")

        return query.scalar()  # type: ignore

    async def read_account_by_username(self, username: str) -> Account:
        stmt = select(Account).where(Account.username == username)
        query = await self.session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist(f"account with username `{username}` does not exist!")

        return query.scalar()  # type: ignore

    async def read_account_by_email(self, email: str) -> Account:
        stmt = select(Account).where(Account.email == email)
        query = await self.session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist(f"account with email `{email}` does not exist!")

        return query.scalar()  # type: ignore

    async def authenticate_user(self, data: LoginRequestSchema) -> Account:
        stmt = select(Account).where(Account.username == data.username)
        query = await self.session.execute(statement=stmt)
        account = query.scalar()

        if not account:
            raise EntityDoesNotExist("wrong username or password!")

        if not pwd_generator.verify_password(
            hash_salt=account.hash_salt,
            password=data.password,
            hashed_password=account.hashed_password,
        ):
            raise PasswordDoesNotMatch("wrong username or password!")

        return account  # type: ignore

    async def is_username_available(self, username: str) -> bool:
        stmt = select(Account.username).select_from(Account).where(Account.username == username)
        query = await self.session.execute(statement=stmt)
        db_username = query.scalar()

        if db_username:
            raise EntityAlreadyExists(f"the username `{username}` is already taken!")  # type: ignore
        return True

    async def is_email_available(self, email: str) -> bool:
        stmt = select(Account.email).select_from(Account).where(Account.email == email)
        query = await self.session.execute(statement=stmt)
        db_email = query.scalar()

        if db_email:
            raise EntityAlreadyExists(f"the username `{email}` is already taken!")  # type: ignore
        return True

    async def is_phone_number_available(self, phone_number: str) -> bool:
        stmt = select(Account.phone_number).select_from(Account).where(Account.phone_number == phone_number)
        query = await self.session.execute(statement=stmt)
        db_phone_number = query.scalar()

        if db_phone_number:
            raise EntityAlreadyExists(f"the username `{phone_number}` is already taken!")  # type: ignore
        return True
