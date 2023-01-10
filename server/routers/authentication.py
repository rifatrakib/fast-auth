from fastapi import APIRouter, Depends, status

from server.crud.user import UserDatabaseAPI
from server.dependencies.session import get_async_session
from server.schemas.user import AccountInResponse, AccountWithToken, UserCreateRequest
from server.security.token import JWTGenerator
from server.utilities.exceptions import EntityAlreadyExists
from server.utilities.http_exceptions import http_exc_400_credentials_bad_signup_request

router = APIRouter(prefix="/user", tags=["authentication"])


@router.post(
    "/register",
    name="user:register",
    response_model=AccountInResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user: UserCreateRequest,
    session: UserDatabaseAPI = Depends(get_async_session(session_type=UserDatabaseAPI)),
) -> AccountInResponse:
    try:
        await session.is_username_available(username=user.username)
        await session.is_email_available(email=user.email)
    except EntityAlreadyExists:
        raise await http_exc_400_credentials_bad_signup_request()

    new_account = await session.create_account(data=user)
    access_token = JWTGenerator.generate_access_token(account=new_account)

    return AccountInResponse(
        id=new_account.id,
        authorized_account=AccountWithToken(
            token=access_token,
            username=new_account.username,
            email=new_account.email,  # type: ignore
            is_verified=new_account.is_verified,
            is_active=new_account.is_active,
            is_logged_in=new_account.is_logged_in,
            created_at=new_account.created_at,
            updated_at=new_account.updated_at,
        ),
    )
