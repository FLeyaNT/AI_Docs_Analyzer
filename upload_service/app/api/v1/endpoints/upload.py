import logging

from fastapi import (
    APIRouter,
    File,
    UploadFile
)

from typing import List


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/upload',
    tags=['Upload'],
)


@router.post(
    path='/files',
)
async def upload_files(
    files: List[UploadFile]
):
    for file in files:
        logger.info(file.filename)
