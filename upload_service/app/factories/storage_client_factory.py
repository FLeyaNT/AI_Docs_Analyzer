from typing import TYPE_CHECKING

from app.clients.s3_storage.base_s3_client import BaseS3Client
from app.clients.s3_storage.aioboto3_client import AioBoto3S3Client
from app.core.config import (
    settings,
    S3BaseConfig
)

if TYPE_CHECKING:
    from app.clients.abc.async_storage_client import (
        AsyncStorageClientAbstract,
    )


class StorageClientFactory:

    @staticmethod
    def create() -> 'AsyncStorageClientAbstract':
        if settings.storage_type == 's3':
            return StorageClientFactory.create_s3_client()

        raise ValueError(
             f'Unknown storage type: {settings.storage_type}'
         )

    @staticmethod
    def create_s3_client() -> BaseS3Client:
        if settings.storage_client == 'aioboto3':
            s3_class = AioBoto3S3Client
        else:
            raise ValueError(
                f'Unknown S3 client: {settings.storage_client}'
            )

        if settings.storage_service == 'yandex':
            config = settings.yandex

        elif settings.storage_service == 'minio':
            config = settings.minio

        else:
            raise ValueError(
                f'Unknown S3 service: {settings.storage_service}'
            )

        return StorageClientFactory.get_current_s3_client(
            s3_class=s3_class,
            config=config
        )

    @staticmethod
    def get_current_s3_client(
        s3_class: type[BaseS3Client],
        config: S3BaseConfig
    ) -> BaseS3Client:
        return s3_class(
            bucket=config.bucket_name,
            access_key=config.access_key,
            secret_key=config.secret_key,
            endpoint_url=config.endpoint_url,
            region_name=config.region
        )
