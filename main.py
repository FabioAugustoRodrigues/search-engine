from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.v1.schema import router as schema_api

from app.core.clients import create_redis_client, close_redis_client
from app.core.settings import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    app.state.redis = create_redis_client(settings.REDIS_URL)
    try:
        yield
    finally:
        print("Shutting down...")
        close_redis_client(app.state.redis)

app = FastAPI(
    title="Search Engine",
    description="",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(schema_api, prefix="/api/v1/schemas", tags=["Schemas"])