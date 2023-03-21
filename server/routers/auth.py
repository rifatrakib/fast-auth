from fastapi import APIRouter, BackgroundTasks, Depends, Path, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from server.cache.account import AccountRedis
from server.core.config import settings
from server.models.user import Account
from server.schemas.account import (
    AccountInformationResponse,
    AuthResponseSchema,
    MessageResponseSchema,
)
from server.security.dependencies import (
    change_email_form,
    email_form_field,
    generate_crud_instance,
    generate_redis_client,
    get_current_active_user,
    new_password_form,
    password_form_field,
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
    http_exc_404_not_found,
)
from server.services.validators import EmailTemplates, Tags
from server.sql.user import AccountCRUD, AccountValidationCRUD

router = APIRouter(prefix="/auth", tags=[Tags.authentication])


@router.post(
    "/signup",
    name="auth:signup",
    summary="Create new account",
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
        subject=f"Account activation for {new_user.username}",
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
    redis: AccountRedis = Depends(generate_redis_client(AccountRedis)),
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
    await redis.set_account_data(user)

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


@router.get(
    "/{account_id}",
    name="account:info",
    summary="Fetch information about an active or non active user",
    response_model=AccountInformationResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_user)],
)
async def read_account_by_id(
    account_id: int = Path(
        title="user ID",
        decription="Unique ID that can be used to distinguish between users.",
    ),
    account: AccountCRUD = Depends(generate_crud_instance(name=AccountCRUD)),
):
    try:
        user = await account.read_account_by_id(account_id)
        return user
    except EntityDoesNotExist:
        raise await http_exc_404_not_found()


@router.patch(
    "/password/update",
    name="account:password-update",
    summary="Update password of the current active user",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def update_user_password(
    current_password: str = Depends(password_form_field),
    new_password: str = Depends(new_password_form),
    account: AccountCRUD = Depends(generate_crud_instance(name=AccountCRUD)),
    current_user: Account = Depends(get_current_active_user),
):
    await account.update_password(
        account_id=current_user.id,
        current_password=current_password,
        new_password=new_password,
    )
    return MessageResponseSchema(msg="Password updated successfully!")


@router.post(
    "/password/forgot",
    name="account:forgot-password",
    summary="Send an email with a secret key to reset password of a user",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def forgot_user_password(
    request: Request,
    task: BackgroundTasks,
    email: EmailStr = Depends(email_form_field),
    account: AccountCRUD = Depends(generate_crud_instance(name=AccountCRUD)),
    validator: AccountValidationCRUD = Depends(generate_crud_instance(name=AccountValidationCRUD)),
):
    try:
        user = await account.read_account_by_email(email=email)
        task.add_task(
            send_email,
            request=request,
            account=user,
            validator=validator,
            base_url=settings.PASSWORD_RESET_URL,
            template_name=EmailTemplates.password_reset,
            subject=f"Password reset for {user.username}",
        )
        return MessageResponseSchema(msg="Please check your email for resetting password")
    except EntityDoesNotExist:
        raise await http_exc_404_not_found()


@router.patch(
    "/password/reset/{validation_key}",
    name="account:reset-password",
    summary="Use secret key sent in mail to verify and reset password",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def reset_user_password(
    validation_key: str,
    new_password: str = Depends(new_password_form),
    account: AccountCRUD = Depends(generate_crud_instance(name=AccountCRUD)),
    validator: AccountValidationCRUD = Depends(generate_crud_instance(name=AccountValidationCRUD)),
):
    try:
        deleted_record = await validator.delete_account_validation(validation_key=validation_key)
        await account.reset_password(
            account_id=deleted_record.account_id,
            new_password=new_password,
        )
        return MessageResponseSchema(msg="Password was reset successfully!")
    except EntityDoesNotExist:
        raise await http_exc_404_key_expired()


@router.post(
    "/change/email",
    name="account:change-email",
    summary="Change email of the current active user",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def change_account_email(
    request: Request,
    task: BackgroundTasks,
    new_email: EmailStr = Depends(change_email_form),
    current_user: Account = Depends(get_current_active_user),
    validator: AccountValidationCRUD = Depends(generate_crud_instance(name=AccountValidationCRUD)),
):
    task.add_task(
        send_email,
        request=request,
        account=current_user,
        validator=validator,
        base_url=settings.EMAIL_CHANGE_URL,
        template_name=EmailTemplates.change_email,
        email=new_email,
        subject=f"Change email for {current_user.username}",
        extras={"new-email": new_email},
    )
    return MessageResponseSchema(msg="Please check your email for confirmation!")
