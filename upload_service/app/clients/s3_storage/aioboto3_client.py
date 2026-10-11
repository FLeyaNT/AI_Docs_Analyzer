import aioboto3
from aiobotocore.client import AioBaseClient
from botocore.config import Config
from botocore.exceptions import (
    ClientError,
    EndpointConnectionError
)

from app.clients.exceptions import (
    StorageAccessError,
    StorageConnectionError,
    StorageNotFoundError,
    StorageOperationError,
)

from app.clients.s3_storage.base_s3_client import BaseS3Client


class AioBoto3S3Client(BaseS3Client):

    def __init__(
        self,
        bucket: str,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        region_name: str
    ) -> None:
        super().__init__(
            bucket=bucket,
            access_key=access_key,
            secret_key=secret_key,
            endpoint_url=endpoint_url,
            region_name=region_name
        )

        self._session: aioboto3.Session | None = None

    def _get_client(self) -> AioBaseClient:
        if not self._session:
            self._session = aioboto3.Session(
                aws_access_key_id=self._access_key,
                aws_secret_access_key=self._secret_key
            )

        return self._session.client(
            's3',
            endpoint_url=self._endpoint_url,
            region_name=self._region_name,
            config=Config(signature_version="s3v4"),
        )

    async def _upload(
        self,
        file_data: bytes,
        file_name: str
    ) -> None:
        try:
            async with self._get_client() as client:
                await client.put_object(
                    Bucket=self._bucket,
                    Key=file_name,
                    Body=file_data
                )

        except EndpointConnectionError as e:
            raise StorageConnectionError() from e

        except ClientError as e:
            self._raise_storage_error(e)

    async def _download(
        self,
        file_name: str
    ) -> bytes:
        ...

    async def _delete(
        self,
        file_name: str
    ) -> None:
        ...

    @staticmethod
    def _raise_storage_error(
        error: ClientError
    ) -> None:
        error_code = error.response.get('Error', {}).get('Code')

        if error_code in {'403', 'AccessDenied'}:
            raise StorageAccessError() from error

        if error_code in {'404', 'NoSuchKey', 'NotFound'}:
            raise StorageNotFoundError() from error

        raise StorageOperationError() from error
