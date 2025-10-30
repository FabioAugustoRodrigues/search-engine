from fastapi import FastAPI

from app.api.v1.schema import router as schema_api

app = FastAPI(
    title="Search Engine",
    description="",
    version="0.1.0"
)

app.include_router(schema_api, prefix="/api/v1/schemas", tags=["Schemas"])