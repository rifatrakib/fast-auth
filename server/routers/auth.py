from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from server.schemas.account import (
    AuthResponseSchema,
    LoginRequestSchema,
    SignupRequestSchema,
)
from server.security.dependencies import generate_crud_instance
from server.security.token import jwt_generator
from server.services.email import send_email
from server.services.exceptions import EntityAlreadyExists
from server.services.messages import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_400_credentials_bad_signup_request,
)
from server.sql.user import AccountCRUD

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/signup",
    name="auth:signup",
    summary="Create new user",
    response_model=AuthResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    payload: SignupRequestSchema,
    task: BackgroundTasks,
    account: AccountCRUD = Depends(generate_crud_instance(name=AccountCRUD)),
):
    try:
        await account.is_username_available(username=payload.username)
        await account.is_email_available(email=payload.email)
    except EntityAlreadyExists:
        raise await http_exc_400_credentials_bad_signup_request()

    new_user = await account.create_account(data=payload)
    task.add_task(send_email, email=new_user.email)
    access_token = jwt_generator.generate_access_token(account=new_user)

    return AuthResponseSchema(token_type="Bearer", access_token=access_token)


@router.post(
    "/signin",
    name="auth:signin",
    summary="Authenticate user for token",
    response_model=AuthResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def signin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    account: AccountCRUD = Depends(generate_crud_instance(name=AccountCRUD)),
):
    try:
        data = LoginRequestSchema(username=form_data.username, password=form_data.password)
        user = await account.authenticate_user(data)
    except Exception:
        raise await http_exc_400_credentials_bad_signin_request()

    access_token = jwt_generator.generate_access_token(account=user)

    return AuthResponseSchema(token_type="Bearer", access_token=access_token)
