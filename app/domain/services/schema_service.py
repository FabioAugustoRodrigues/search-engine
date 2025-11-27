from app.infrastructure.providers.redis_provider import RedisProvider
from app.infrastructure.providers.redis_search_provider import RedisSearchProvider
from app.domain.exceptions.domain_exception import SchemaAlreadyExistsError, ErrorWhileCreatingSchema

import json

class SchemaService:
    def __init__(
        self, 
        redis_provider: RedisProvider,
        redis_search_provider: RedisSearchProvider
    ):
        self._redis_provider = redis_provider
        self._redis_search_provider = redis_search_provider

    def create_schema(self, schema) -> str:
        """
        Create a schema in Redis and a Redisearch index, 
        given a CreateSchemaRequest instance.
        
        Raises a SchemaAlreadyExistsError if a schema with the same name already exists.
        Raises an ErrorWhileCreatingSchema if there is an error while creating the schema.
        """
        if self.get_schema_by_name(schema.name) is not None:
            raise SchemaAlreadyExistsError(schema.name)

        if not self.set_schema_by_name(schema.name, schema.json()):
            raise ErrorWhileCreatingSchema(schema.name)
            
        data = json.loads(schema.json())
        fields = data["fields"] 

        self._redis_search_provider.create_index(
            self._generate_index_name(schema.name), 
            fields
        )
        
        return schema.name

    def get_schemas(self):
        """
        Retrieves all schemas from Redis.
        """
        prefix = "schema"
        return self._redis_provider.list_all(prefix)

    def get_schema_by_name(self, name):
        """
        Retrieves a schema from Redis by its name.
        """
        schema_name = self._generate_index_name(name)
        return self._redis_provider.get(schema_name)

    def set_schema_by_name(self, name, value):
        """
        Stores a schema in Redis by its name.
        """
        schema_name = self._generate_index_name(name)
        return self._redis_provider.set(schema_name, value)
    
    def _generate_index_name(self, schema_name):
        """
        Generates a Redis Index Name for a schema based on its name.
        """
        return f"idx:{schema_name}"