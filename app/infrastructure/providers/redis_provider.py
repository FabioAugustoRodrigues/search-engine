import redis
from typing import Any, Optional


class RedisProvider:
    """Infrastructure provider that manages Redis connections and common data operations."""

    def __init__(self, client: redis.Redis):
        """
        Initialize the provider with an existing Redis client.

        :param client: An active redis.Redis instance.
        """
        self._client = client

    def set(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """Store a key-value pair in Redis, optionally with expiration time."""
        return bool(self._client.set(key, value, ex=ex))

    def list_all(self, prefix: str) -> list[str]:
        """Return all Redis keys that start with the given prefix using SCAN (non-blocking)."""
        cursor = 0
        keys = []

        while True:
            cursor, batch = self._client.scan(cursor=cursor, match=f"{prefix}:*", count=100)
            keys.extend(batch)
            if cursor == 0:
                break

        return [k.decode() if isinstance(k, bytes) else k for k in keys]

    def get(self, key: str) -> Optional[str]:
        """Retrieve a value from Redis by key."""
        return self._client.get(key)

    def delete(self, key: str) -> int:
        """Delete a key from Redis."""
        return self._client.delete(key)

    def exists(self, key: str) -> bool:
        """Check if a key exists in Redis."""
        return bool(self._client.exists(key))

    def increment(self, key: str, amount: int = 1) -> int:
        """Increment a numeric value by a given amount."""
        return self._client.incrby(key, amount)

    def expire(self, key: str, seconds: int) -> bool:
        """Set an expiration time (in seconds) for a key."""
        return bool(self._client.expire(key, seconds))

    def flush(self) -> None:
        """Remove all keys from the current Redis database (use with caution)."""
        self._client.flushdb()