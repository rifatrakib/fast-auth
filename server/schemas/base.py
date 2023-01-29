from datetime import datetime
from typing import Any

from pydantic import BaseModel

from server.services.formatters import (
    format_datetime_into_isoformat,
    format_dict_key_to_camel_case,
)


class BaseSchemaORM(BaseModel):
    class Config:
        orm_mode: bool = True
        validate_assignment: bool = True
        allow_population_by_field_name: bool = True
        json_encoders: dict = {datetime: format_datetime_into_isoformat}
        alias_generator: Any = format_dict_key_to_camel_case
