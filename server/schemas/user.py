from pydantic import Field

from server.schemas.base import BaseSchemaAPI


class UpdateUserPassword(BaseSchemaAPI):
    password: str = Field(
        title="password",
        decription="""
            Password containing at least 1 uppercase letter, 1 lowercase letter,
            1 number, 1 character that is neither letter nor number, and
            between 8 to 32 characters.
        """,
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,64}$",
        min_length=8,
        max_length=64,
    )
