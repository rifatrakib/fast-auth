from typing import Sequence

from sqlalchemy import select

from server.models.user import Account
from server.schemas.user import SignupRequestSchema
from server.security.password import pwd_generator
from server.services.exceptions import EntityDoesNotExist
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
