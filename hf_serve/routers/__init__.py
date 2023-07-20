from fastapi import APIRouter

from hf_serve.routers import inference

api_router = APIRouter()
api_router.include_router(inference.router, tags=["inference"])
