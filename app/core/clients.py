import redis

from app.core.settings import settings


def create_redis_client(url: str | None = None) -> redis.Redis:
    target_url = url or settings.REDIS_URL
    return redis.Redis.from_url(target_url, decode_responses=True)


def close_redis_client(client: redis.Redis | None) -> None:
    if client is None:
        return
    try:
        client.close()
    except Exception:
        pass