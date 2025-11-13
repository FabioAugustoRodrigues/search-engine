from pydantic import BaseModel, Field, model_validator
from typing import List, Literal

class FieldDefinition(BaseModel):
    name: str
    type: Literal["text", "numeric", "tag"]
    sortable: bool = False
    weight: float = 1.0

class CreateSchemaRequest(BaseModel):
    name: str = Field(..., pattern=r"^[a-zA-Z0-9_]+$", description="Schema name must be alphanumeric/underscore")
    fields: List[FieldDefinition]

    # Check if fields are not empty
    @model_validator(mode="after")
    def validate_fields_not_empty(self):
        if not self.fields:
            raise ValueError("At least one field must be provided in 'fields'")
        return self

    # Example for json_schema_extra
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "products_schema_name",
                    "fields": [
                        {
                            "name": "name",
                            "type": "text",
                            "sortable": True,
                            "weight": 5.0
                        },
                        {
                            "name": "price",
                            "type": "numeric",
                            "sortable": True
                        },
                    ]
                }
            ]
        }
    }