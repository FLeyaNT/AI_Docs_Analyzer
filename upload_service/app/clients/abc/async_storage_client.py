from abc import ABC, abstractmethod


class AsyncStorageClientAbstract(ABC):

    @abstractmethod
    async def upload_file(
        self,
        file_data: bytes,
        file_name: str
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def download_file(
        self,
        file_name: str
    ) -> bytes:
        raise NotImplementedError()

    @abstractmethod
    async def delete_file(
        self,
        file_name: str
    ) -> bool:
        raise NotImplementedError()
