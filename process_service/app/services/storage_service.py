from app.clients.boto_s3_client import Boto3S3Client, boto3_s3_client


class StorageService:

    def __init__(
        self,
        client: Boto3S3Client
    ):
        self._client = client

    def download_file(
        self,
        file_name: str
    ) -> bytes:
        return self._client.download(
            file_name=file_name
        )


storage_service = StorageService(boto3_s3_client)
