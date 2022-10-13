from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str
    algorithm: str
    secret_key: str
    access_token_expire_minutes: int
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_from_name: str

    class Config:
        env_file = ".env"


settings = Settings().dict()


def read_config(name):
    return settings.get(name, None)
