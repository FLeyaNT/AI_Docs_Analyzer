import logging
from functools import wraps
from typing import (
    Awaitable,
    Callable,
    ParamSpec,
    TypeVar,
    TYPE_CHECKING
)

from app.clients.exceptions import (
    StorageAccessError,
    StorageConnectionError,
    StorageNotFoundError,
    StorageOperationError
)

if TYPE_CHECKING:
    from app.clients.s3_storage.base_s3_client import BaseS3Client


logger = logging.getLogger(__name__)

P = ParamSpec('P')
T = TypeVar('T')


def handle_storage_errors(
    operation: str
) -> Callable[
    [Callable[P, Awaitable[T]]],
    Callable[P, Awaitable[T]]
]:
    def decorator(
        func: Callable[P, Awaitable[T]]
    ) -> Callable[P, Awaitable[T]]:
        @wraps(func)
        async def wrapper(
            self: 'BaseS3Client',
            *args: P.args,
            **kwargs: P.kwargs
        ) -> T:
            file_name = kwargs.get('file_name')

            try:
                return await func(self, *args, **kwargs)

            except StorageNotFoundError as e:
                logger.debug(
                    'File not found: '
                    'operation=%s, bucket=%s, file_name=%s',
                    operation,
                    self.bucket,
                    file_name,
                )
                raise

            except StorageAccessError as e:
                logger.error(
                    'Storage access denied: '
                    'operation=%s, bucket=%s, file_name=%s, error=%s',
                    operation,
                    self.bucket,
                    file_name,
                    e,
                )
                raise

            except StorageConnectionError as e:
                logger.error(
                    'Storage access denied: '
                    'operation=%s, bucket=%s, file_name=%s, error=%s',
                    operation,
                    self.bucket,
                    file_name,
                    e,
                )
                raise

            except StorageOperationError as e:
                logger.exception(
                    'Unexpected error: '
                    'operation=%s, bucket=%s, file_name=%s, error=%s',
                    operation,
                    self.bucket,
                    file_name,
                    e,
                )
                raise

        return wrapper

    return decorator
