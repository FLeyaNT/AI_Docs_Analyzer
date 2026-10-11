from typing import Annotated, TYPE_CHECKING
from functools import lru_cache

from fastapi import Depends

from app.factories.storage_client_factory import (
    StorageClientFactory
)
from app.services.storage_service import StorageService
from app.celery.celery_app import celery_app

if TYPE_CHECKING:
    from app.clients.abc.async_storage_client import (
        AsyncStorageClientAbstract
    )


@lru_cache(maxsize=1)
def get_storage_client() -> 'AsyncStorageClientAbstract':
    return StorageClientFactory.create()

StorageClientDep = Annotated[
    'AsyncStorageClientAbstract',
    Depends(get_storage_client)
]


def get_storage_service(
    storage_client: StorageClientDep
) -> StorageService:
    return StorageService(
        storage_client=storage_client,
        celery=celery_app
    )

StorageServiceDep = Annotated[
    StorageService,
    Depends(get_storage_service)
]
