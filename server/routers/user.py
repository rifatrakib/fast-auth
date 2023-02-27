from fastapi import APIRouter, BackgroundTasks, Depends, Form, Path, Request, status
from pydantic import EmailStr

from server.core.config import settings
from server.models.user import Account
from server.schemas.account import MessageResponseSchema
from server.schemas.user import UserInformationResponse
from server.security.dependencies import (
    generate_crud_instance,
    get_current_active_user,
    new_password_form,
)
from server.services.email import send_email
from server.services.exceptions import EntityDoesNotExist
from server.services.messages import http_exc_404_key_expired, http_exc_404_not_found
from server.services.validators import Tags
from server.sql.user import AccountCRUD, AccountValidationCRUD

router = APIRouter(prefix="/users", tags=[Tags.users])


@router.get(
    "/{user_id}",
    name="user:info",
    summary="Fetch information about an active or non active user",
    response_model=UserInformationResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_user)],
)
async def read_user_by_id(
    user_id: int = Path(
        title="user ID",
        decription="Unique ID that can be used to distinguish between users.",
    ),
    account: AccountCRUD = Depends(generate_crud_instance(name=AccountCRUD)),
):
    try:
        user = await account.read_account_by_id(user_id)
        return user
    except EntityDoesNotExist:
        raise await http_exc_404_not_found()


@router.patch(
    "/password/update",
    name="user:password-update",
    summary="Update password of the current active user",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def update_user_password(
    current_password: str = Form(
        alias="currentPassword",
        title="current password",
        decription="""
            Password containing at least 1 uppercase letter, 1 lowercase letter,
            1 number, 1 character that is neither letter nor number, and
            between 8 to 32 characters.
        """,
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,64}$",
        min_length=8,
        max_length=64,
    ),
    account: AccountCRUD = Depends(generate_crud_instance(name=AccountCRUD)),
    current_user: Account = Depends(get_current_active_user),
    new_password: str = Depends(new_password_form),
):
    await account.update_password(
        account_id=current_user.id,
        current_password=current_password,
        new_password=new_password,
    )
    return MessageResponseSchema(msg="Password updated successfully!")


@router.post(
    "/password/forgot",
    name="user:forgot-password",
    summary="Send an email with a secret key to reset password of a user",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def forgot_user_password(
    request: Request,
    task: BackgroundTasks,
    email: EmailStr = Form(
        title="email",
        decription="Email of the account for which to reset password.",
    ),
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
            template_name="password-reset",
            base_url=settings.PASSWORD_RESET_URL,
        )
        return MessageResponseSchema(msg="Please check your email for resetting password")
    except EntityDoesNotExist:
        raise await http_exc_404_not_found()


@router.patch(
    "/password/reset/{validation_key}",
    name="user:reset-password",
    summary="Use secret key sent in mail to verify and reset password",
    response_model=MessageResponseSchema,
    status_code=status.HTTP_200_OK,
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
