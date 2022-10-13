from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from ..config import read_config

mailer = ConnectionConfig(
    MAIL_USERNAME=read_config("mail_username"),
    MAIL_PASSWORD=read_config("mail_password"),
    MAIL_FROM=read_config("mail_from"),
    MAIL_PORT=read_config("mail_port"),
    MAIL_SERVER=read_config("mail_server"),
    MAIL_FROM_NAME=read_config("mail_from_name"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_email(email):
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[email],
        body="<p>html email trial as background task</p>",
        subtype=MessageType.html,
    )
    fm = FastMail(mailer)
    await fm.send_message(message)
