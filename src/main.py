import os
import sys

import fastapi
import uvicorn
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from fastapi.exceptions import RequestValidationError
from loguru import logger
from src.api.public_endpoints import router as public_api_endpoint_router
from src.config.events import (
    execute_backend_server_event_handler,
    terminate_backend_server_event_handler,
)
from src.config.manager import settings
from src.utilities.core.exception_handlers import (
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)

def custom_openapi(app: fastapi.FastAPI):
    """
    Custom OpenAPI schema generator.
    """
    if app.openapi_schema:
        return app.openapi_schema

    from fastapi.openapi.utils import get_openapi

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}

    openapi_schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


def initialize_backend_application() -> fastapi.FastAPI:
    app = fastapi.FastAPI(**settings.set_backend_app_attributes)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )

    app.add_event_handler(
        "startup",
        execute_backend_server_event_handler(backend_app=app),
    )

    app.add_event_handler(
        "shutdown",
        terminate_backend_server_event_handler(backend_app=app),
    )

    # Register exception handlers
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    # public router
    app.include_router(router=public_api_endpoint_router, prefix=settings.API_PREFIX)

    app.openapi = lambda: custom_openapi(app)

    return app


backend_app: fastapi.FastAPI = initialize_backend_application()

if __name__ == "__main__":
    uvicorn.run(
        app="main:backend_app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        workers=settings.SERVER_WORKERS,
        log_level=settings.LOGGING_LEVEL,
    )
