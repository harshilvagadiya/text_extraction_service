import decouple
from src.config.settings.base import BackendBaseSettings

from src.config.settings.environment import Environment
from src.config.settings.local import BackendLocalSettings


class BackendSettingsFactory:
    def __init__(self, environment: str):
        self.environment = environment
    def __call__(self) -> BackendBaseSettings:
        if self.environment == Environment.LOCAL.value:
            return BackendLocalSettings()

def get_settings() -> BackendBaseSettings:
    return BackendSettingsFactory(environment=decouple.config("ENVIRONMENT", default="DEVELOPMENT", cast=str))()

settings: BackendBaseSettings = get_settings()
