from fastapi import APIRouter, Depends, Form, HTTPException, status

from server.models.user import Account
from server.schemas.account import MessageResponseSchema
from server.security.dependencies import generate_crud_instance, get_current_active_user
from server.services.validators import Tags
from server.sql.user import AccountCRUD

router = APIRouter(prefix="/users", tags=[Tags.users])


@router.get("/{id}")
async def read_user_by_id(id: int):
    return {"id": id}


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
