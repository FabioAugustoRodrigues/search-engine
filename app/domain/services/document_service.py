from app.infrastructure.providers.redis_provider import RedisProvider
from app.infrastructure.providers.redis_search_provider import RedisSearchProvider
from app.domain.exceptions.domain_exception import SchemaNotFoundError

from .schema_service import SchemaService

import uuid
import json

class DocumentService:
    def __init__(
        self, 
        redis_provider: RedisProvider,
        redis_search_provider: RedisSearchProvider,
        schema_service: SchemaService
    ):
        self._redis_provider = redis_provider
        self._redis_search_provider = redis_search_provider
        self._schema_service = schema_service

    def index_document(self, schema_name: str, document_fields: dict) -> str:
        """
        Index a document in RedisSearch under the given schema.
        Raises SchemaNotFoundError if the schema doesn't exist.
        """
        existing_schema = self._schema_service.get_schema_by_name(schema_name)
        if existing_schema is None:
            raise SchemaNotFoundError(schema_name)

        schema = json.loads(existing_schema)
        schema_fields = schema["fields"]

        schema_index = self._schema_service._generate_index_name(schema_name)
        document_id = self._generate_document_id()

        indexed_fields = {**document_fields}
        indexed_fields["id"] = document_id

        document_index = self._redis_search_provider.add_document(schema_index, document_id, indexed_fields)

        return document_index

    def _generate_document_id(self) -> str:
        """
        Generate a unique document ID.
        """
        return str(uuid.uuid4())
