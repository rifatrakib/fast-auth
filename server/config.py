from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str

    class Config:
        env_file = ".env"


settings = Settings().dict()


def read_config(name):
    return settings.get(name, None)
