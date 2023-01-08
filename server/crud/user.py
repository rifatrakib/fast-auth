from typing import Sequence

from sqlalchemy import select

from server.crud.base import CRUD
from server.models.user import Account
from server.schemas.user import UserCreateRequest
from server.security.password import pwd_generator
from server.utilities.exceptions import EntityDoesNotExist


class UserDatabaseAPI(CRUD):
    async def create_account(self, data: UserCreateRequest) -> Account:
        new_account = Account(**data.dict(), is_logged_in=True)
        new_account.set_hash_salt(hash_salt=pwd_generator.generate_salt)
        new_account.set_hashed_password(
            hashed_password=pwd_generator.generate_hashed_password(
                hash_salt=new_account.hash_salt,
                new_password=data.password,
            )
        )

        self.session.add(instance=new_account)
        await self.session.commit()
        await self.session.refresh(instance=new_account)
        return new_account

    async def read_accounts(self, limit: int = 20, page: int = 1) -> Sequence[Account]:
        stmt = select(Account).offset((page - 1) * limit).limit(limit)
        query = await self.session.execute(statement=stmt)
        return query.scalars().all()

    async def read_account_by_id(self, id: int) -> Account:
        stmt = select(Account).where(Account.id == id)
        query = await self.session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist("Account with id `{id}` does not exist!")

        return query.scalar()

    async def read_account_by_email(self, email: str) -> Account:
        stmt = select(Account).where(Account.email == email)
        query = await self.session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist("Account with email `{email}` does not exist!")

        return query.scalar()

    async def read_account_by_username(self, username: str) -> Account:
        stmt = select(Account).where(Account.username == username)
        query = await self.session.execute(statement=stmt)

        if not query:
            return False

        return query.scalar()

    async def authenticate_user(self, username: str, password: str) -> Account:
        user = self.read_account_by_username(username)
        if not user:
            return False

        if not pwd_generator.is_password_authenticated(
            hash_salt=user.hash_salt,
            password=password,
            hashed_password=user.hashed_password,
        ):
            return False

        return user
