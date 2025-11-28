from fastapi import APIRouter, Depends

from app.core.dependencies import get_document_service
from app.domain.services.document_service import DocumentService
from app.schemas.document import IndexDocumentRequest

router = APIRouter()

@router.post("/")
def index_document(
    req: IndexDocumentRequest,
    document_service: DocumentService = Depends(get_document_service)
):
    value = document_service.index_document(
        schema_name=req.schema_name, 
        document_fields=req.fields
    )
    
    return {
        "message": "Document indexed successfully",
        "document_index": value
    }