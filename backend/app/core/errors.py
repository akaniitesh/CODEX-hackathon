from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ApiError(Exception):
    """Base class for expected application errors."""

    def __init__(self, message: str, status_code: int) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ErrorResponse(BaseModel):
    """Structured error payload returned by API handlers."""

    detail: str
    code: str


def register_exception_handlers(app: FastAPI) -> None:
    """Register structured exception handlers."""

    @app.exception_handler(ApiError)
    async def handle_api_error(
        _request: Request,
        exc: ApiError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(detail=exc.message, code="api_error").model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        _request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors(), "code": "validation_error"},
        )

