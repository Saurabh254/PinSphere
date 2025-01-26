from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from .base_exception import ServerError


async def server_exception_handler(request: Request, exc: ServerError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": type(exc).__name__, "detail": exc.message},
        headers=exc.headers,
    )


def add_exception_handler(app: FastAPI):
    app.add_exception_handler(ServerError, server_exception_handler)  # type: ignore
