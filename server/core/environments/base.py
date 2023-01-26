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

    # token config
    ALGORITHM: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRY_MINUTES: str

    class Config:
        env_file = ".env"
