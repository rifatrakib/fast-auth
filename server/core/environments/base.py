from typing import Union

from pydantic import BaseSettings, EmailStr, HttpUrl, RedisDsn


class BaseConfig(BaseSettings):
    APP_NAME: str
    MODE: str

    # RDBMS configs
    RDS_HOST: str
    RDS_PORT: str
    RDS_USER: str
    RDS_PASS: str
    RDS_NAME: str

    REDIS_URL: RedisDsn

    # password hashing config
    PASSWORD_HASH_ALGORITHM: str
    SALT_HASH_ALGORITHM: str
    HASH_SALT: str

    # token config
    JWT_SECRET_KEY: str
    JWT_SUBJECT: str
    JWT_ALGORITHM: str
    JWT_TOKEN_PREFIX: str
    JWT_MIN: int
    JWT_HOUR: int
    JWT_DAY: int

    # mail server config
    MAIL_USERNAME: Union[EmailStr, str]
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    USE_CREDENTIALS: bool

    # random generator config
    RANDOM_BYTE_LENGTH: int
    ACTIVATION_URL: HttpUrl
    PASSWORD_RESET_URL: HttpUrl
    EMAIL_CHANGE_URL: HttpUrl

    class Config:
        env_file = ".env"
