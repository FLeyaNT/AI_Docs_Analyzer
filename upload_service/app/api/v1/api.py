from fastapi import APIRouter

from .endpoints import upload


router_v1 = APIRouter(
    prefix='/v1',
)

router_v1.include_router(upload.router)
