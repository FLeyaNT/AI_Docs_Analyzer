import uuid
import os
import asyncio
from typing import TYPE_CHECKING, Coroutine, Any

from celery import Celery

if TYPE_CHECKING:
    from app.clients.abc.async_storage_client import (
        AsyncStorageClientAbstract,
    )


class StorageService:

    def __init__(
        self,
        storage_client: 'AsyncStorageClientAbstract',
        celery: Celery
    ) -> None:
        self._storage_client = storage_client
        self._celery = celery

    async def upload_file(
        self,
        file_data: bytes,
        file_name: str
    ) -> None:
        await self._storage_client.upload_file(
            file_data=file_data,
            file_name=file_name
        )

        self._celery.send_task(
            name='process_service.process_file',
            args=[file_name],
        )

    @staticmethod
    def _get_extension(file_name: str) -> str:
        return os.path.splitext(file_name)[-1]

    @staticmethod
    def _get_new_file_name(
        file_id: str,
        extension: str
    ) -> str:
        return f'{file_id}.{extension}'

    async def upload_files(
        self,
        files: dict[str, bytes],
    ) -> None:
        tasks: list[Coroutine[Any, Any, None]] = []

        for file_name, file_data in files.items():
            file_id = str(uuid.uuid4())
            extension = self._get_extension(file_name)
            new_name = self._get_new_file_name(
                file_id=file_id,
                extension=extension
            )

            tasks.append(
                self.upload_file(
                    file_data=file_data,
                    file_name=new_name
                )
            )

        await asyncio.gather(*tasks)

    async def delete_file(self):
        ...