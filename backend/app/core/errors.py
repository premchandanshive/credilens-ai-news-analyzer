"""
CrediLens — Standard Error Classes & Envelope Handlers
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any

class AppException(Exception):
    def __init__(self, code: str, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class InvalidInputException(AppException):
    def __init__(self, message: str = "Invalid input data provided."):
        super().__init__("INVALID_INPUT", message, status.HTTP_400_BAD_REQUEST)

class NotFoundException(AppException):
    def __init__(self, message: str = "The requested resource was not found."):
        super().__init__("NOT_FOUND", message, status.HTTP_404_NOT_FOUND)

class UnauthorizedException(AppException):
    def __init__(self, message: str = "Authentication required to access this resource."):
        super().__init__("UNAUTHORIZED", message, status.HTTP_401_UNAUTHORIZED)

class PayloadTooLargeException(AppException):
    def __init__(self, message: str = "Input content exceeds the maximum allowed size."):
        super().__init__("PAYLOAD_TOO_LARGE", message, status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

class BackendUnavailableException(AppException):
    def __init__(self, message: str = "The analyzer service is currently unavailable."):
        super().__init__("BACKEND_UNAVAILABLE", message, status.HTTP_503_SERVICE_UNAVAILABLE)

def create_error_response(code: str, message: str, status_code: int = 400) -> JSONResponse:
    """Format standard CrediLens API error envelope."""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": code,
                "message": message
            }
        }
    )
