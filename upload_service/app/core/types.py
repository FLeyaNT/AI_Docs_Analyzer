from typing import Annotated

from fastapi import UploadFile

from pydantic import WithJsonSchema


UploadFileList = Annotated[
    list[UploadFile],
    WithJsonSchema({
        'type': 'array',
        'items': {
            'type': 'string',
            'format': 'binary'
        }
    })
]
