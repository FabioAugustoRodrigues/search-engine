from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.api.v1.schema import router as schema_api
from app.api.v1.document import router as document_api

from app.core.clients import create_redis_client, close_redis_client
from app.core.settings import settings
from app.core.responses import ApiResponse
from app.domain.exceptions.domain_exception import DomainException


# --- Create FastAPI app ---
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
    lifespan=lifespan,
    default_response_class=ApiResponse
)



# --- Register routers ---
app.include_router(schema_api, prefix="/api/v1/schemas", tags=["Schemas"])
app.include_router(document_api, prefix="/api/v1/documents", tags=["Documents"])



# --- Global DomainException handler ---
@app.exception_handler(DomainException)
async def handle_domain_exception(_, exc: DomainException):
    """
    Handles all domain-level exceptions raised by services.
    Returns a consistent JSON error response.
    """
    return ApiResponse(
        content={
            "error": exc.error_code,
            "detail": str(exc),
        },
        status_code=exc.status_code
    )