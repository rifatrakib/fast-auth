from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    APP_NAME: str
    MODE: str

    # RDBMS configs
    RDS_HOST: str
    RDS_PORT: str
    RDS_USER: str
    RDS_PASS: str
    RDS_NAME: str

    # password hashing config
    PASSWORD_HASH_ALGORITHM: str
    SALT_HASH_ALGORITHM: str
    HASH_SALT: str

    # token config
    JWT_SECRET_KEY: str
    JWT_SUBJECT: str
    JWT_ALGORITHM: str
    JWT_TOKEN_PREFIX: str
    JWT_MIN: str
    JWT_HOUR: str
    JWT_DAY: str

    class Config:
        env_file = ".env"
