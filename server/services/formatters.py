from datetime import datetime, timezone


def format_datetime_into_isoformat(timestamp: datetime) -> str:
    return timestamp.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


def format_dict_key_to_camel_case(key: str) -> str:
    return "".join(word if idx == 0 else word.capitalize() for idx, word in enumerate(key.split("_")))
