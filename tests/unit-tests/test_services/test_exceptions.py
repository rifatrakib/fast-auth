import pytest

from server.services.exceptions import (
    EntityAlreadyExists,
    EntityDoesNotExist,
    PasswordDoesNotMatch,
    UserNotActive,
)


def test_entity_does_not_exist_exception():
    with pytest.raises(EntityDoesNotExist):
        raise EntityDoesNotExist("Data does not exist in the database.")


def test_entity_already_exists_exception():
    with pytest.raises(EntityAlreadyExists):
        raise EntityAlreadyExists("Data already exists in the database.")


def test_password_does_not_match_exception():
    with pytest.raises(PasswordDoesNotMatch):
        raise PasswordDoesNotMatch("Passwords do not match.")


def test_user_not_active_exception():
    with pytest.raises(UserNotActive):
        raise UserNotActive("User is not active.")
