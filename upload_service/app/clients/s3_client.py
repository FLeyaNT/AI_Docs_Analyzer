import logging
from io import BytesIO

from miniopy_async import Minio
from miniopy_async.error import S3Error

from app.clients.exceptions import (
    StorageConnectionError,
    StorageException
)
from app.core.config import settings
from app.clients.abc.async_storage_client import (
    AsyncStorageClientAbstract,
)


logger = logging.getLogger(__name__)


class S3Client(AsyncStorageClientAbstract):

    def __init__(self) -> None:
        self.bucket = settings.s3.bucket_name
        self.endpoint = settings.s3.endpoint
        self.access_key = settings.s3.access_key
        self.secret_key = settings.s3.secret_key
        self.external_url = settings.s3.external_url
        self.region = settings.s3.region


        try:
            self.client = Minio(
                endpoint=settings.minio.endpoint,
                access_key=settings.minio.access_key,
                secret_key=settings.minio.secret_key,
                secure=settings.minio.secure
            )
            self.bucket = settings.minio.bucket_name
        except Exception as e:
            logger.error(f'Failed to initialize s3 client: {e}')
            raise StorageConnectionError(f'Failed to connect to S3: {e}')

    async def _ensure_bucket_exists(self) -> None:
        try:
            if not await self.client.bucket_exists(self.bucket):
                await self.client.make_bucket(self.bucket)
                logger.info(f'Bucket "{self.bucket}" created')
            else:
                logger.info(f'Bucket "{self.bucket}" already exists')
        except S3Error as e:
            logger.error(f'Failed to create bucket: {e}')
            raise StorageBucketError(f'Failed to ensure bucket: {e}')

    def _create_object_url(
        self,
        file_name: str
    ) -> str:
        return f'{settings.minio.external_url}/{self.bucket}/{file_name}'

    async def upload_file(
        self,
        file_data: bytes,
        file_name: str
    ) -> str:
        try:
            data_stream = BytesIO(file_data)
            await self._ensure_bucket_exists()

            await self.client.put_object(
                bucket_name=self.bucket,
                object_name=file_name,
                data=data_stream,
                length=len(file_data),
                content_type='application/octet-stream',
            )
            return self._create_object_url(file_name)
        except S3Error as e:
            logger.error(f'Failed to upload file: {e}')
            raise StorageUploadError(f"Failed to upload file '{file_name}': {e}")
        except Exception as e:
            logger.error(f'Unexpected error during upload: {e}')
            raise StorageUploadError(f"Unexpected error uploading file '{file_name}': {e}")

    async def download_file(
        self,
        file_name: str
    ) -> bytes:
        try:
            async with await self.client.get_object(
                bucket_name=self.bucket,
                object_name=file_name
            ) as response:
                data = await response.read()
                return data
        except S3Error as e:
            if "NoSuchKey" in str(e) or "NotFound" in str(e):
                logger.warning(f'File "{file_name}" not found')
                raise StorageFileNotFoundError(f"File '{file_name}' not found in storage")
            logger.error(f'Failed to download file "{file_name}": {e}')
            raise StorageDownloadError(f"Failed to download file '{file_name}': {e}")
        except Exception as e:
            logger.error(f'Unexpected error during download: {e}')
            raise StorageDownloadError(f"Unexpected error downloading file '{file_name}': {e}")

    async def delete_file(
        self,
        file_name: str
    ) -> bool:
        try:
            await self.client.remove_object(
                bucket_name=self.bucket,
                object_name=file_name,
            )
            return True
        except S3Error as e:
            if "NoSuchKey" in str(e) or "NotFound" in str(e):
                logger.warning(f'File "{file_name}" not found for deletion')
                raise StorageFileNotFoundError(f"File '{file_name}' not found in storage")
            logger.error(f'Failed to delete file "{file_name}": {e}')
            raise StorageDeleteError(f"Failed to delete file '{file_name}': {e}")
        except Exception as e:
            logger.error(f'Unexpected error during deletion: {e}')
            raise StorageDeleteError(f"Unexpected error deleting file '{file_name}': {e}")

    async def file_exists(
        self,
        file_name: str
    ) -> bool:
        try:
            await self.client.stat_object(
                bucket_name=self.bucket,
                object_name=file_name
            )
            return True
        except S3Error as e:
            if "NoSuchKey" in str(e) or "NotFound" in str(e):
                return False
            logger.error(f'Failed to check file existence "{file_name}": {e}')
            raise StorageException(f"Failed to check file existence '{file_name}': {e}")
        except Exception as e:
            logger.error(f'Unexpected error checking file existence: {e}')
            raise StorageException(f"Unexpected error checking file existence '{file_name}': {e}")
