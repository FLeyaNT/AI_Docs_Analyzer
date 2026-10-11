import logging
from pathlib import Path
from typing import Literal

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)
from pydantic import BaseModel

from .constants import LOG_DEFAULT_FORMAT


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class LoggingConfig(BaseModel):
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


class RunConfig(BaseModel):
    host: str = '127.0.0.1'
    port: int = 8000
    reload: bool = True


class FastAPIConfig(BaseModel):
    title: str = 'Download Service API'


class S3BaseConfig(BaseModel):
    access_key: str
    secret_key: str
    bucket_name: str
    host: str
    port: int | None = None
    secure: bool = False
    region: str | None

    @property
    def endpoint_url(self) -> str:
        protocol = 'https' if self.secure else 'http'
        url = self.host

        if self.port:
            url = f'{url}:{self.port}'

        return f'{protocol}://{url}'


class YandexS3Config(S3BaseConfig):
    host: str = 'https://storage.yandexcloud.net'
    region: str = 'ru-central1'
    secure: bool = True


class MinioS3Config(S3BaseConfig):
    host: str = 'localhost'
    port: int = 9000
    region: str | None = None
    secure: bool = False


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter='__',
        env_file=BASE_DIR / '.env'
    )

    storage_type: str = 's3'
    storage_client: str = 'aioboto3'
    storage_service: str = 'yandex'

    run: RunConfig = RunConfig()
    fastapi: FastAPIConfig = FastAPIConfig()
    logging: LoggingConfig = LoggingConfig()
    yandex: YandexS3Config
    minio: MinioS3Config


settings = Settings()
