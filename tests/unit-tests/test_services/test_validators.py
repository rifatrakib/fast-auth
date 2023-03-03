from server.services.validators import EmailTemplates, Gender, Tags


def test_gender_enum():
    assert Gender.male.value == "m"
    assert Gender.female.value == "f"


def test_tags_enum():
    assert Tags.authentication.value == "Authentication"
    assert Tags.users.value == "Users"
    assert Tags.server_health.value == "Health"


def test_email_templates_enum():
    assert EmailTemplates.account_activation.value == "account-activation"
    assert EmailTemplates.password_reset.value == "password-reset"
