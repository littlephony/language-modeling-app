from fastapi import Request, status
from fastapi.logger import logger
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def get_error_response(request, exc) -> dict:
    """
    Handling generic error
    """
    return {"error": True, "message": str(exc)}


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handling request validation error
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=get_error_response(request, exc),
    )


async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=get_error_response(request, exc),
    )
