from fastapi import Request
from app.infrastructure.providers.redis_provider import RedisProvider


def get_redis_provider(request: Request) -> RedisProvider:
    """
    Dependency function that provides a RedisProvider instance.
    
    This function retrieves the Redis client from the application state
    and returns a RedisProvider instance. This allows for dependency injection
    in route handlers.
    """
    redis_client = request.app.state.redis
    return RedisProvider(redis_client)

