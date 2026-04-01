from fastapi import APIRouter
from app.api.routers import catalogs, products

api_router = APIRouter()
api_router.include_router(catalogs.router)
api_router.include_router(products.router)
