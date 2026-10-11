import logging

from fastapi import (
    APIRouter,
    File,
    UploadFile
)

from typing import TYPE_CHECKING

from app.api.dependencies import StorageServiceDep


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/upload',
    tags=['Upload'],
)


@router.post(
    path='/files',
    status_code=204
)
async def upload_files(
    files: list[UploadFile],
    storage_service: StorageServiceDep
):
    files_dict: dict[str, bytes] = {}

    for file in files:
        file_name = file.filename if file.filename else 'file.pdf'
        files_dict[file_name] = await file.read()

    await storage_service.upload_files(files_dict)
