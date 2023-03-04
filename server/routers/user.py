from datetime import datetime
from typing import Union

from fastapi import APIRouter, Depends

from server.schemas.user import UserResponseSchema
from server.security.dependencies import (
    birthday_form_field,
    first_name_form_field,
    gender_form_field,
    last_name_form_field,
    middle_name_form_field,
)
from server.services.validators import Tags

router = APIRouter(prefix="/users", tags=[Tags.users])


@router.post("/", response_model=UserResponseSchema)
async def create_new_user(
    first_name: str = Depends(first_name_form_field(optional=False)),
    middle_name: Union[str, None] = Depends(middle_name_form_field),
    last_name: str = Depends(last_name_form_field(optional=False)),
    gender: str = Depends(gender_form_field),
    birthday: datetime = Depends(birthday_form_field),
):
    return {
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "gender": gender,
        "birthday": birthday,
    }
