import logging
from typing import Literal

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)

from .constants import LOG_DEFAULT_FORMAT


class LoggingConfig(BaseSettings):
    log_level: Literal[
        'debug',
        'info',
        'warning',
        'error',
        'critical',
    ] = 'info'
    log_format: str = LOG_DEFAULT_FORMAT

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[
            self.log_level.upper()
        ]


class RunConfig(BaseSettings):
    host: str = '127.0.0.1'
    port: int = '8000'
    reload: bool = True


class FastAPIConfig(BaseSettings):
    title: str = 'Download Serivce API'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False
    )

    run: RunConfig = RunConfig()
    fastapi: FastAPIConfig = FastAPIConfig()
    logging: LoggingConfig = LoggingConfig()


settings = Settings()
