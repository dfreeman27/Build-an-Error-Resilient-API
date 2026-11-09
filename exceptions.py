from fastapi.responses import JSONResponse
from email import message


class NotFoundError(Exception):
    """Raised when a requested resource does not exist."""
    def __init__(self, message: str):

        super().__init__(message)
        self.message = message

class DuplicateError(Exception):
    """Raised when creating a resource would violate a uniqueness constraint."""
    def __init__(self, message: str):
    
        super().__init__(message)
        self.message = message

class AppValidationError(Exception):
    """Raised for domain-level validation failures (beyond Pydantic schema checks)."""
    def __init__(self, message: str):
    
        super().__init__(message)
        self.message = message




async def not_found_handler(request, exc: NotFoundError):
    """Handles NotFoundError → 404 response."""
    async def not_found_handler(request, exc: NotFoundError):
        return JSONResponse(
            status_code=404,
            content={
                "error": "NotFoundError",
                "message": exc.message,
                "status_code": 404
            }
        )

async def duplicate_handler(request, exc: DuplicateError):
    """Handles DuplicateError → 409 response."""
    async def duplicate_handler(request, exc: DuplicateError):
        return JSONResponse(
            status_code=409,
            content={
                "error": "DuplicateError",
                "message": exc.message,
                "status_code": 409
            }
        )


async def app_validation_handler(request, exc: AppValidationError):
    """Handles AppValidationError → 422 response."""
    async def app_validation_handler(request, exc: AppValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "error": "AppValidationError",
                "message": exc.message,
                "status_code": 422
            }
        )