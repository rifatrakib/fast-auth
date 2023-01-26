from server.core.config import BaseConfig


class StagingConfig(BaseConfig):
    DEBUG: bool = False
    MODE: str = "Staging"
