from fastapi import APIRouter, BackgroundTasks, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from server.core.config import settings
from server.schemas.account import AuthResponseSchema, MessageResponseSchema
from server.security.dependencies import (
    email_form_field,
    generate_crud_instance,
    new_password_form,
    phone_number_form_field,
    username_form_field,
)
from server.security.token import jwt_generator
from server.services.email import send_email
from server.services.exceptions import (
    EntityAlreadyExists,
    EntityDoesNotExist,
    PasswordDoesNotMatch,
    UserNotActive,
)
from server.services.messages import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_400_credentials_bad_signup_request,
    http_exc_400_inactive_user,
    http_exc_404_key_expired,
)
from server.services.validators import EmailTemplates, Tags
from server.sql.user import AccountCRUD, AccountValidationCRUD

router = APIRouter(prefix="/auth", tags=[Tags.authentication])


@router.post(
    "/signup",
    name="auth:signup",
    summary="Create new user",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    request: Request,
    task: BackgroundTasks,
    username: str = Depends(username_form_field),
    email: EmailStr = Depends(email_form_field),
    phone_number: str = Depends(phone_number_form_field),
    password: str = Depends(new_password_form),
    account: AccountCRUD = Depends(generate_crud_instance(name=AccountCRUD)),
    validator: AccountValidationCRUD = Depends(generate_crud_instance(name=AccountValidationCRUD)),
):
    try:
        await account.is_username_available(username=username)
        await account.is_email_available(email=email)
    except EntityAlreadyExists:
        raise await http_exc_400_credentials_bad_signup_request()

    new_user = await account.create_account(
        username=username,
        email=email,
        phone_number=phone_number,
        password=password,
    )

    task.add_task(
        send_email,
        request=request,
        account=new_user,
        validator=validator,
        base_url=settings.ACTIVATION_URL,
        template_name=EmailTemplates.account_activation,
    )

    return MessageResponseSchema(msg="Please check your email to activate your account")


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
        user = await account.authenticate_user(
            username=form_data.username,
            password=form_data.password,
        )
    except EntityDoesNotExist:
        raise await http_exc_400_credentials_bad_signin_request()
    except UserNotActive:
        raise await http_exc_400_inactive_user()
    except PasswordDoesNotMatch:
        raise await http_exc_400_credentials_bad_signin_request()

    access_token = jwt_generator.generate_access_token(account=user)

    return AuthResponseSchema(token_type="Bearer", access_token=access_token)


@router.get(
    "/activate-account/{validation_key}",
    name="auth:activation",
    summary="Activate user account with random validation key",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def activate_account(
    validation_key: str,
    account: AccountCRUD = Depends(generate_crud_instance(name=AccountCRUD)),
    validator: AccountValidationCRUD = Depends(generate_crud_instance(name=AccountValidationCRUD)),
):
    try:
        account_to_activate = await validator.delete_account_validation(validation_key=validation_key)
        await account.activate_account(account_to_activate.account_id)
    except EntityDoesNotExist:
        raise await http_exc_404_key_expired()
    return MessageResponseSchema(msg="Your account has been activated")
