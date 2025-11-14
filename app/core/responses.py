from fastapi.responses import JSONResponse
from pydantic import BaseModel

from typing import Any


class ApiResponseStructure(BaseModel):
    details: Any
    status_code: int

class ApiResponse(JSONResponse):
    def __init__(self, content: Any, status_code: int = 200, *args, **kwargs) -> None:
        content = ApiResponseStructure(details=content, status_code=status_code).model_dump()
        super().__init__(content, status_code, *args, **kwargs)