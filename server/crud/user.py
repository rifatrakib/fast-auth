from typing import Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.sql import functions

from server.crud.base import CRUD
from server.models.user import Account
from server.schemas.user import UserCreateRequest, UserUpdateRequest
from server.security.password import pwd_generator
from server.utilities.exceptions import EntityAlreadyExists, EntityDoesNotExist


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
            raise EntityDoesNotExist(f"Account with id `{id}` does not exist!")

        return query.scalar()

    async def read_account_by_email(self, email: str) -> Account:
        stmt = select(Account).where(Account.email == email)
        query = await self.session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist(f"Account with email `{email}` does not exist!")

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

    async def update_account_by_id(self, id: int, data: UserUpdateRequest) -> Account:
        select_stmt = select(Account).where(Account.id == id)
        query = await self.session.execute(statement=select_stmt)
        update_account = query.scalar()

        if not update_account:
            raise EntityDoesNotExist(f"Account with id `{id}` does not exist!")

        update_stmt = update(table=Account).where(Account.id == update_account.id).values(updated_at=functions.now())

        new_account_data = {}
        for key, value in data.dict().items():
            if value and key == "password":
                new_account_data["hash_salt"] = pwd_generator.generate_salt
                new_account_data["hashed_password"] = pwd_generator.generate_hashed_password(
                    hash_salt=new_account_data["hash_salt"],
                    new_password=data.password,
                )
            elif value:
                new_account_data[key] = value

        update_stmt = update_stmt.values(**new_account_data)
        await self.session.execute(statement=update_stmt)
        await self.session.commit()
        await self.session.refresh(instance=update_account)
        return update_account

    async def delete_account_by_id(self, id: int) -> str:
        select_stmt = select(Account).where(Account.id == id)
        query = await self.session.execute(select_stmt)
        delete_account = query.scalar()

        if not delete_account:
            raise EntityDoesNotExist(f"Account with id `{id}` does not exist!")

        stmt = delete(Account).where(Account.id == delete_account.id)
        await self.session.execute(stmt)
        await self.session.commit()
        return f"Account with id '{id}' is successfully deleted!"

    async def is_username_available(self, username: str) -> bool:
        stmt = select(Account.username).select_from(Account).where(Account.username == username)
        query = await self.session.execute(stmt)
        db_username = query.scalar()

        if not db_username:
            raise EntityAlreadyExists(f"The username `{username}` is already taken!")
        return True

    async def is_email_available(self, email: str) -> bool:
        stmt = select(Account.email).select_from(Account).where(Account.email == email)
        query = await self.session.execute(stmt)
        db_email = query.scalar()

        if not db_email:
            raise EntityAlreadyExists(f"The email `{email}` is already taken!")
        return True
