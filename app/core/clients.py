import redis

from app.core.settings import settings


def create_redis_client(url: str | None = None) -> redis.Redis:
    """
    Creates a Redis client instance from a given URL or the default URL in settings.
    """
    target_url = url or settings.REDIS_URL
    return redis.Redis.from_url(target_url, decode_responses=True)


def close_redis_client(client: redis.Redis | None) -> None:
    """
    Closes a Redis client instance, ignoring any exceptions that may occur.

    If the client is None, the function does nothing.
    """
    if client is None:
        return
    try:
        client.close()
    except Exception:
        pass