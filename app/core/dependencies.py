from fastapi import Request, Depends

from app.infrastructure.providers.redis_provider import RedisProvider
from app.domain.services.schema_service import SchemaService


def get_redis_provider(request: Request) -> RedisProvider:
    """
    Dependency function that provides a RedisProvider instance.
    
    This function retrieves the Redis client from the application state
    and returns a RedisProvider instance. This allows for dependency injection
    in route handlers.
    """
    redis_client = request.app.state.redis
    return RedisProvider(redis_client)

def get_redis_search_provider(request: Request) -> RedisSearchProvider:
    """
    Dependency function that provides a RedisSearchProvider instance.
    
    This function retrieves the Redis client from the application state
    and returns a RedisSearchProvider instance. This allows for dependency injection
    in route handlers.
    """
    redis_client = request.app.state.redis
    return RedisSearchProvider(redis_client)

def get_schema_service(redis_provider: RedisProvider = Depends(get_redis_provider)):
    """
    Dependency function that provides a SchemaService instance.

    This function retrieves a RedisProvider instance and returns a SchemaService
    instance. This allows for dependency injection in route handlers.
    """
    return SchemaService(redis_provider)