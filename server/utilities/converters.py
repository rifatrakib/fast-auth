import inspect
from datetime import datetime, timezone

from pydantic import BaseModel


def convert_datetime_to_isoformat(date_time: datetime) -> str:
    return date_time.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


def convert_dict_key_to_camel_case(dict_key: str) -> str:
    return "".join(word if idx == 0 else word.capitalize() for idx, word in enumerate(dict_key.split("_")))


def optional(*fields):
    """Decorator function used to modify a pydantic model's fields to all be
    optional.

    Alternatively, you can  also pass the field names that should be made optional as arguments
    to the decorator.
    Taken from https://github.com/samuelcolvin/pydantic/issues/1223#issuecomment-775363074
    """

    def dec(_cls):
        for field in fields:
            _cls.__fields__[field].required = False
        return _cls

    if fields and inspect.isclass(fields[0]) and issubclass(fields[0], BaseModel):
        cls = fields[0]
        fields = cls.__fields__
        return dec(cls)

    return dec
