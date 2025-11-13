from app.infrastructure.providers.redis_provider import RedisProvider

class SchemaService:
    def __init__(self, redis_provider: RedisProvider):
        self._redis_provider = redis_provider

    def create_schema(self, schema):
        self._redis_provider.set("example_key", "example_value", ex=3600)
        value = self._redis_provider.get("example_key")

        return value