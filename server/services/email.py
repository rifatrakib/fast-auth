from typing import Dict

from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr, HttpUrl

from server.core.config import settings
from server.models.user import Account
from server.sql.user import AccountValidationCRUD

templates = Jinja2Templates(directory="server/templates")


def get_mail_config():
    conf = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
        MAIL_STARTTLS=settings.MAIL_STARTTLS,
        MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
        USE_CREDENTIALS=settings.USE_CREDENTIALS,
    )
    return conf


async def send_email(
    request: Request,
    account: Account,
    validator: AccountValidationCRUD,
    template_name: str,
    subject: str,
    base_url: HttpUrl,
    email: EmailStr = None,
    extras: Dict[str, str] = {},
):
    account_validator = await validator.create_account_validation(account.id)
    validation_key = account_validator.validation_key
    url = f"{base_url}/{validation_key}"

    if extras:
        for key, value in extras.items():
            url = f"{url}?{key}={value}"

    template = templates.TemplateResponse(
        f"{template_name}.html",
        {
            "request": request,
            "subject": subject,
            "url": url,
            "username": account.username,
        },
    )

    if email:
        recipients = [email]
    else:
        recipients = [account.email]

    html = template.body.decode("utf-8")
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=html,
        subtype=MessageType.html,
    )

    mailing_agent = FastMail(get_mail_config())
    await mailing_agent.send_message(message)
