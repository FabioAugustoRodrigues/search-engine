from app.infrastructure.providers.redis_provider import RedisProvider
from app.infrastructure.providers.redis_search_provider import RedisSearchProvider

from app.domain.exceptions.domain_exception import InvalidFieldError

from .schema_service import SchemaService

from app.validators.fields_validator import validate_fields

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
        """
        schema_json = self._schema_service.get_schema_by_name_or_fail(schema_name)
        schema = json.loads(schema_json)
        schema_fields = schema["fields"]

        self._check_for_fields(schema_fields, document_fields)

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

    def _check_for_fields(self, schema_fields: str, document_fields: dict):
        extra, missing = validate_fields(document_fields, schema_fields)

        if extra:
            extra_fields = ", ".join(extra)
            raise InvalidFieldError(message=f"There are extra fields in the document that are not in the schema: {extra_fields}.")

        if missing:
            missing_fields = ", ".join(missing)
            raise InvalidFieldError(message=f"There are missing fields in the document that are in the schema: {missing_fields}.")