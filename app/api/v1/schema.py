from fastapi import APIRouter, Depends
from app.core.dependencies import get_redis_provider
from app.infrastructure.providers.redis_provider import RedisProvider

router = APIRouter()

@router.post("/")
def create_schema(redis: RedisProvider = Depends(get_redis_provider)):
    """
    Example route demonstrating dependency injection of RedisProvider.
    
    The RedisProvider is automatically injected via FastAPI's dependency system.
    You can now use all RedisProvider methods directly.
    """
    redis.set("example_key", "example_value", ex=3600)
    value = redis.get("example_key")
    
    return {
        "message": "Schema created successfully",
        "redis_value": value
    }