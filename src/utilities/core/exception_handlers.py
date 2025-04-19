from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel
from typing import Any, List, Optional


# Custom API Response Model
class CustomAPIResponse(BaseModel):
    status: str
    message: str
    errors: Optional[List[dict]] = None
    data: Optional[Any] = None

    @classmethod
    def success(cls, data: Any = None, message: str = "Request successful.", status_code: int = 200):
        return cls(
            status="success",
            message=message,
            errors=None,
            data=data
        )

    @classmethod
    def error(cls, message: str, errors: Optional[List[dict]] = None, status_code: int = 400):
        return cls(
            status="error",
            message=message,
            errors=errors or [],
            data=None
        )

    @classmethod
    def validation_error(cls, errors: List[dict], status_code: int = 422):
        return cls(
            status="error",
            message="Validation error",
            errors=errors,
            data=None
        )



async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc.errors()} | Path: {request.url.path}")
    serialized_errors = [
        {"loc": error["loc"], "msg": error["msg"], "type": error["type"]}
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content=CustomAPIResponse.validation_error(errors=serialized_errors).dict()
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)} | Path: {request.url.path}")
    return JSONResponse(
        status_code=500,
        content=CustomAPIResponse.error(
            message="An unexpected error occurred.",
            errors=[{"details": str(exc)}],
        ).dict()
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP exception occurred: {exc.detail} | Path: {request.url.path}")
    message = exc.detail if exc.detail else "An HTTP error occurred."

    return JSONResponse(
        status_code=exc.status_code,
        content=CustomAPIResponse.error(
            message=message,
            errors=[{"detail": exc.detail}] if exc.detail else [],
        ).dict()
    )
