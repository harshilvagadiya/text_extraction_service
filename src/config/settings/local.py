from src.config.settings.base import BackendBaseSettings
from src.config.settings.environment import Environment


class BackendLocalSettings(BackendBaseSettings):
    DESCRIPTION: str | None = "Local Environment."
    DEBUG: bool = True
    ENVIRONMENT: Environment = Environment.LOCAL
