from fastapi import FastAPI
from app.api.api import api_router
from app.core.config import settings

def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    application.include_router(api_router, prefix=settings.API_V1_STR)
    return application

app = create_application()

@app.get("/", tags=["Health"])
def root():
    return {"message": "Welcome to Shop Inventory Management System API"}
