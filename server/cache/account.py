from pydantic import parse_raw_as

from server.cache.base import RedisBase
from server.models.user import Account
from server.schemas.account import AccountInformationResponse


class AccountRedis(RedisBase):
    async def set_account_data(self, user: Account):
        value = AccountInformationResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            phone_number=user.phone_number,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        await self.redis.set(f"auth-{user.id}", value.json(), ex=30)

    async def get_account_data(self, user_id: int):
        user_data = await self.redis.get(f"auth-{user_id}")
        if user_data:
            return parse_raw_as(type_=AccountInformationResponse, b=user_data)
