from fastapi import APIRouter, Depends, Form, HTTPException, Path, status

from server.models.user import Account
from server.schemas.account import MessageResponseSchema
from server.schemas.user import UserInformationResponse
from server.security.dependencies import generate_crud_instance, get_current_active_user
from server.services.exceptions import EntityDoesNotExist
from server.services.messages import http_exc_404_not_found
from server.services.validators import Tags
from server.sql.user import AccountCRUD

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
        print(f"{user = }")
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
    new_password: str = Form(
        title="new password",
        decription="""
            Password containing at least 1 uppercase letter, 1 lowercase letter,
            1 number, 1 character that is neither letter nor number, and
            between 8 to 32 characters.
        """,
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,64}$",
        min_length=8,
        max_length=64,
    ),
    repeat_new_password: str = Form(
        title="repeat new password",
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
):
    if new_password != repeat_new_password:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail={"msg": "New passwords does not match!"},
        )

    await account.update_password(
        account_id=current_user.id,
        current_password=current_password,
        new_password=new_password,
    )
    return MessageResponseSchema(msg="Password updated successfully!")
