from fastapi import APIRouter, Depends

from app.core.dependencies import get_schema_service
from app.domain.services.schema_service import SchemaService
from app.schemas.schema import CreateSchemaRequest

router = APIRouter()

@router.post("/")
def create_schema(
    req: CreateSchemaRequest,
    schema_service: SchemaService = Depends(get_schema_service)
):
    value = schema_service.create_schema(req)
    
    return {
        "message": "Schema created successfully",
        "schema_name": value
    }