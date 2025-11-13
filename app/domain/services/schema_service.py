from app.infrastructure.providers.redis_provider import RedisProvider
from app.domain.exceptions.domain_exception import SchemaAlreadyExistsError

class SchemaService:
    def __init__(self, redis_provider: RedisProvider):
        self._redis_provider = redis_provider

    def create_schema(self, schema):
        """
        Create a schema in Redis, given a CreateSchemaRequest instance.
        
        Raises a SchemaAlreadyExistsError if a schema with the same name already exists.
        """
        if self.get_schema_by_name(schema.name) is not None:
            raise SchemaAlreadyExistsError(schema.name)
        
        return self.set_schema_by_name(schema.name, schema.json())

    def get_schema_by_name(self, name):
        """
        Retrieves a schema from Redis by its name.
        """
        schema_name = self._generate_schema_key(name)
        return self._redis_provider.get(schema_name)

    def set_schema_by_name(self, name, value):
        """
        Stores a schema in Redis by its name.
        """
        schema_name = self._generate_schema_key(name)
        return self._redis_provider.set(schema_name, value)
    
    def _generate_schema_key(self, schema_name):
        """
        Generates a Redis key for a schema based on its name.
        """
        return f"schema:{schema_name}"