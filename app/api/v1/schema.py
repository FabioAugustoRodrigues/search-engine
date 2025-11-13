from fastapi import APIRouter, Depends

from app.core.dependencies import get_redis_provider
from app.infrastructure.providers.redis_provider import RedisProvider
from app.schemas.schema import CreateSchemaRequest

router = APIRouter()

@router.post("/")
def create_schema(
    req: CreateSchemaRequest,
    redis: RedisProvider = Depends(get_redis_provider)
):
    redis.set("example_key", "example_value", ex=3600)
    value = redis.get("example_key")
    
    return {
        "message": "Schema created successfully",
        "redis_value": value
    }