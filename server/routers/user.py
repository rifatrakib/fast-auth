from datetime import datetime
from typing import Union

from fastapi import APIRouter, Depends, status

from server.models.user import Account
from server.schemas.user import UserResponseSchema
from server.security.dependencies import (
    birthday_form_field,
    first_name_form_field,
    gender_form_field,
    generate_crud_instance,
    get_current_active_user,
    last_name_form_field,
    middle_name_form_field,
)
from server.services.exceptions import EntityAlreadyExists
from server.services.messages import http_exc_409_conflict
from server.services.validators import Tags
from server.sql.user import UserCRUD

router = APIRouter(prefix="/users", tags=[Tags.users])


@router.post(
    "/",
    name="user:create-user",
    summary="Create new user",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_user(
    first_name: str = Depends(first_name_form_field(optional=False)),
    middle_name: Union[str, None] = Depends(middle_name_form_field),
    last_name: str = Depends(last_name_form_field(optional=False)),
    gender: str = Depends(gender_form_field),
    birthday: datetime = Depends(birthday_form_field),
    user: UserCRUD = Depends(generate_crud_instance(name=UserCRUD)),
    current_user: Account = Depends(get_current_active_user),
):
    try:
        new_user = await user.create_user(
            account_id=current_user.id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            gender=gender,
            birthday=birthday,
        )
    except EntityAlreadyExists:
        raise await http_exc_409_conflict(f"user profile for account_id {current_user.id} already exists")
    return {
        "first_name": new_user.first_name,
        "middle_name": new_user.middle_name,
        "last_name": new_user.last_name,
        "gender": new_user.gender,
        "birthday": new_user.birthday,
    }
