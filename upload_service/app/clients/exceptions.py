class StorageException(Exception):
    pass


class StorageConnectionError(StorageException):
    pass


class StorageAccessError(StorageException):
    pass


class StorageNotFoundError(StorageException):
    pass


class StorageOperationError(StorageException):
    pass
