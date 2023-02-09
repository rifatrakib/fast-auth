from fastapi import APIRouter, Depends

from server.schemas.account import SignupRequestSchema, SignupResponseSchema
from server.schemas.token import AccountToken
from server.security.dependencies import generate_crud_instance
from server.security.token import jwt_generator
from server.services.exceptions import EntityAlreadyExists
from server.services.messages import http_exc_400_credentials_bad_signup_request
from server.sql.user import AccountCRUD

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/signup",
    name="auth:signup",
    summary="Create new user",
    response_model=SignupResponseSchema,
)
async def register_user(
    payload: SignupRequestSchema,
    account: AccountCRUD = Depends(generate_crud_instance(name=AccountCRUD)),
):
    try:
        await account.is_username_available(username=payload.username)
        await account.is_email_available(email=payload.email)
    except EntityAlreadyExists:
        raise await http_exc_400_credentials_bad_signup_request()

    new_user = await account.create_account(data=payload)
    access_token = jwt_generator.generate_access_token(account=new_user)

    return SignupResponseSchema(
        id=new_user.id,
        authentication_token=AccountToken(
            token=access_token,
            username=new_user.username,
            email=new_user.email,
            phone_number=new_user.phone_number,
            is_verified=new_user.is_verified,
            is_active=new_user.is_active,
            is_logged_in=new_user.is_logged_in,
            created_at=new_user.created_at,
            updated_at=new_user.updated_at,
        ),
    )
