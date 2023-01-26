from functools import lru_cache

from server.core.environments.base import BaseConfig


class SettingsFactory:
    def __init__(self, mode: str):
        self.mode = mode

    def __call__(self) -> BaseConfig:
        if self.mode == "development":
            return BaseConfig()


@lru_cache()
def get_settings() -> SettingsFactory:
    return SettingsFactory(mode="development")()


settings: SettingsFactory = get_settings()
