from datetime import datetime
from typing import Any

from pydantic import BaseConfig, BaseModel

from server.utilities.converters import (
    convert_datetime_to_isoformat,
    convert_dict_key_to_camel_case,
)


class SchemaConfigBase(BaseModel):
    class Config(BaseConfig):
        orm_mode: bool = True
        validate_assignment: bool = True
        allow_population_by_field_name: bool = True
        json_encoders: dict = {datetime: convert_datetime_to_isoformat}
        alias_generator: Any = convert_dict_key_to_camel_case
