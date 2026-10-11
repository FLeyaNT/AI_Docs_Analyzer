import boto3
from botocore.config import Config


class Boto3S3Client:

    def __init__(
        self,
        bucket: str,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        region_name: str | None = None,
    ) -> None:
        self._bucket = bucket

        self._client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint_url,
            region_name=region_name,
            config=Config(signature_version="s3v4"),
        )

    def download(self, file_name: str) -> bytes:
        response = self._client.get_object(
            Bucket=self._bucket,
            Key=file_name,
        )

        return response["Body"].read()


boto3_s3_client = Boto3S3Client(
    bucket='files-bucket',
    access_key='admin',
    secret_key='password',
    endpoint_url='http://localhost:9000',
)
