from abc import ABC, abstractmethod
import logging

from app.clients.abc.async_storage_client import (
    AsyncStorageClientAbstract,
)
from app.clients.decorators import handle_storage_errors


logger = logging.getLogger(__name__)


class BaseS3Client(
    AsyncStorageClientAbstract,
    ABC
):

    def __init__(
        self,
        bucket: str,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        region_name: str
    ) -> None:
        self._bucket = bucket
        self._access_key = access_key
        self._secret_key = secret_key
        self._endpoint_url = endpoint_url
        self._region_name = region_name

    @handle_storage_errors('upload')
    async def upload_file(
        self,
        file_data: bytes,
        file_name: str
    ) -> None:
        await self._upload(
            file_data=file_data,
            file_name=file_name
        )

        logger.info(
            'File uploaded successfully: bucket=%s, file_name=%s, size=%s',
            self._bucket,
            file_name,
            len(file_data)
        )

    @handle_storage_errors('download')
    async def download_file(
        self,
        file_name: str
    ) -> bytes:
        file = await self._download(file_name)

        logger.info(
            'File downloaded successfully: '
            'bucket=%s, file_name=%s, size=%s',
            self._bucket,
            file_name,
            len(file)
        )

        return file

    @handle_storage_errors('delete')
    async def delete_file(
        self,
        file_name: str
    ) -> bool:
        await self._delete(file_name)

        logger.info(
            'File deleted successfully: '
            'bucket=%s, file_name=%s',
            self._bucket,
            file_name
        )

        return True

    @abstractmethod
    async def _upload(
        self,
        file_data: bytes,
        file_name: str
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def _download(
        self,
        file_name: str
    ) -> bytes:
        raise NotImplementedError

    @abstractmethod
    async def _delete(
        self,
        file_name: str
    ) -> None:
        raise NotImplementedError
