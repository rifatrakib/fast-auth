from enum import Enum


class Gender(str, Enum):
    male = "m"
    female = "f"


class Tags(str, Enum):
    authentication = "Authentication"
    users = "Users"
    server_health = "Health"


class EmailTemplates(str, Enum):
    account_activation = "account-activation"
    change_email = "change-email"
    password_reset = "password-reset"  # pragma: allowlist secret
