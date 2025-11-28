class DomainException(Exception):
    """Base class for all domain-level exceptions."""

    status_code: int = 400
    error_code: str = "domain_error"

    def __init__(self, message: str = "", *, status_code: int = None, error_code: str = None):
        super().__init__(message)
        if status_code:
            self.status_code = status_code
        if error_code:
            self.error_code = error_code

class SchemaAlreadyExistsError(DomainException):
    """Exception raised when a schema with the same name already exists."""

    status_code = 409
    error_code = "schema_already_exists"

    def __init__(self, schema_name: str):
        message = f"Schema '{schema_name}' already exists."
        super().__init__(message)

class ErrorWhileCreatingSchema(DomainException):
    """Exception raised when an error occurs while creating a schema."""

    status_code = 500
    error_code = "error_while_creating_schema"

    def __init__(self, schema_name: str):
        message = f"There was an error while creating schema '{schema_name}'."
        super().__init__(message)

class SchemaNotFoundError(DomainException):
    """Exception raised when a schema is not found."""

    status_code = 404
    error_code = "schema_not_found"

    def __init__(self, schema_name: str):
        message = f"Schema '{schema_name}' not found."
        super().__init__(message)