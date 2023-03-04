from datetime import datetime, timedelta
from typing import Sequence, Union

from pydantic import EmailStr
from sqlalchemy import delete, func, select, update
from sqlalchemy.exc import IntegrityError

from server.models.user import Account, AccountValidation, User
from server.security.password import pwd_generator
from server.security.token import generate_account_validation_token
from server.services.exceptions import (
    EntityAlreadyExists,
    EntityDoesNotExist,
    PasswordDoesNotMatch,
    UserNotActive,
)
from server.sql.base import SQLBase


class AccountCRUD(SQLBase):
    async def create_account(
        self,
        username: str,
        email: EmailStr,
        phone_number: str,
        password: str,
    ) -> Account:
        new_account = Account(
            username=username,
            email=email,
            phone_number=phone_number,
        )
        new_account.hash_salt = pwd_generator.generate_salt
        new_account.hashed_password = pwd_generator.generate_hashed_password(
            hash_salt=new_account.hash_salt,
            password=password,
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
        account = query.scalar()

        if not account:
            raise EntityDoesNotExist(f"account with id `{id}` does not exist!")

        return account  # type: ignore

    async def read_account_by_username(self, username: str) -> Account:
        stmt = select(Account).where(Account.username == username)
        query = await self.session.execute(statement=stmt)
        account = query.scalar()

        if not account:
            raise EntityDoesNotExist(f"account with username `{username}` does not exist!")

        return account  # type: ignore

    async def read_account_by_email(self, email: str) -> Account:
        stmt = select(Account).where(Account.email == email)
        query = await self.session.execute(statement=stmt)
        account = query.scalar()

        if not account:
            raise EntityDoesNotExist(f"account with email `{email}` does not exist!")

        return account  # type: ignore

    async def authenticate_user(self, username: str, password: str) -> Account:
        stmt = select(Account).where(Account.username == username)
        query = await self.session.execute(statement=stmt)
        account = query.scalar()

        if not account:
            raise EntityDoesNotExist("wrong username or password!")

        if not account.is_active:
            raise UserNotActive("account is not active! please activate through email.")

        if not pwd_generator.verify_password(
            hash_salt=account.hash_salt,
            password=password,
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

    async def activate_account(self, account_id: int) -> Account:
        select_stmt = select(Account).where(Account.id == account_id)
        query = await self.session.execute(statement=select_stmt)
        update_account = query.scalar()

        if not update_account:
            raise EntityDoesNotExist(f"account with id `{account_id}` does not exist!")  # type: ignore

        update_stmt = (
            update(Account)
            .where(Account.id == update_account.id)
            .values(
                is_active=True,
                updated_at=func.now(),
            )
        )
        await self.session.execute(statement=update_stmt)
        await self.session.commit()
        await self.session.refresh(instance=update_account)

        return update_account

    async def update_password(
        self,
        account_id: int,
        current_password: str,
        new_password: str,
    ) -> Account:
        select_stmt = select(Account).where(Account.id == account_id)
        query = await self.session.execute(statement=select_stmt)
        update_account = query.scalar()

        if not update_account:
            raise EntityDoesNotExist(f"Account with id `{id}` does not exist!")  # type: ignore

        if not pwd_generator.verify_password(
            hash_salt=update_account.hash_salt,
            password=current_password,
            hashed_password=update_account.hashed_password,
        ):
            raise PasswordDoesNotMatch("current password is wrong!")

        updated_hash_salt = pwd_generator.generate_salt
        updated_hashed_password = pwd_generator.generate_hashed_password(
            hash_salt=updated_hash_salt,
            password=new_password,
        )

        update_stmt = (
            update(Account)
            .where(Account.id == update_account.id)
            .values(
                updated_at=func.now(),
                hash_salt=updated_hash_salt,
                hashed_password=updated_hashed_password,
            )
        )

        await self.session.execute(statement=update_stmt)
        await self.session.commit()
        await self.session.refresh(instance=update_account)

        return update_account  # type: ignore

    async def reset_password(self, account_id: int, new_password: str) -> Account:
        select_stmt = select(Account).where(Account.id == account_id)
        query = await self.session.execute(statement=select_stmt)
        update_account = query.scalar()

        if not update_account:
            raise EntityDoesNotExist(f"Account with id `{id}` does not exist!")  # type: ignore

        updated_hash_salt = pwd_generator.generate_salt
        updated_hashed_password = pwd_generator.generate_hashed_password(
            hash_salt=updated_hash_salt,
            password=new_password,
        )

        update_stmt = (
            update(Account)
            .where(Account.id == update_account.id)
            .values(
                updated_at=func.now(),
                hash_salt=updated_hash_salt,
                hashed_password=updated_hashed_password,
            )
        )

        await self.session.execute(statement=update_stmt)
        await self.session.commit()
        await self.session.refresh(instance=update_account)

        return update_account  # type: ignore


class AccountValidationCRUD(SQLBase):
    async def create_account_validation(self, account_id: int) -> AccountValidation:
        try:
            validation_key = generate_account_validation_token()
            new_record = AccountValidation(account_id=account_id, validation_key=validation_key)
            self.session.add(new_record)
            await self.session.commit()
            await self.session.refresh(instance=new_record)
            return new_record
        except IntegrityError:
            await self.session.rollback()
            old_record = await self.fetch_account_validation(account_id=account_id)
            return old_record

    async def fetch_account_validation(self, account_id: int) -> AccountValidation:
        stmt = select(AccountValidation).where(AccountValidation.account_id == account_id)
        query = await self.session.execute(statement=stmt)
        record = query.scalar()

        if not record:
            raise EntityDoesNotExist(f"no record with account_id `{account_id}` found!")

        return record  # type: ignore

    async def delete_account_validation(self, validation_key: str) -> AccountValidation:
        stmt = select(AccountValidation).where(
            AccountValidation.validation_key == validation_key,
            AccountValidation.created_at > datetime.now() - timedelta(minutes=5),
        )
        query = await self.session.execute(statement=stmt)
        account = query.scalar()

        if not account:
            raise EntityDoesNotExist(f"no record with validation_key `{validation_key}` found!")

        stmt = delete(AccountValidation).where(AccountValidation.id == account.id)
        await self.session.execute(statement=stmt)
        await self.session.commit()

        return account


class UserCRUD(SQLBase):
    async def create_user(
        self,
        account_id: int,
        first_name: str,
        middle_name: Union[str, None],
        last_name: str,
        gender: Union[str, None],
        birthday: Union[datetime, None],
    ) -> User:
        stmt = select(User).where(User.account_id == account_id)
        query = await self.session.execute(statement=stmt)
        account = query.scalar()

        if account:
            raise EntityAlreadyExists(f"user with account_id {account_id} already exists")

        new_user = User(
            account_id=account_id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            gender=gender,
            birthday=birthday,
        )

        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(instance=new_user)
        return new_user
