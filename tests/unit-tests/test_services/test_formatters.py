from datetime import datetime

from server.services.formatters import (
    format_datetime_into_isoformat,
    format_dict_key_to_camel_case,
)


def test_format_dict_key_to_camel_case():
    assert format_dict_key_to_camel_case("APP_NAME") == "appName"
    assert format_dict_key_to_camel_case("app_name") == "appName"


def test_format_datetime_into_isoformat():
    timestamp = datetime(2023, 2, 5, 11, 44, 39, 272446)
    assert format_datetime_into_isoformat(timestamp) == "2023-02-05T11:44:39.272446Z"
