import logging
import time
from contextlib import asynccontextmanager

import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, Request
from fastapi_pagination import add_pagination
from sqlalchemy import text
from starlette.middleware.cors import CORSMiddleware

from core.database.session_manager import get_sync_session
from pin_sphere import api
from pin_sphere.exception_handling import add_exception_handler

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting PinSphere API")
    db = next(get_sync_session())
    db.query(text("select 1"))
    db.close()
    yield


app = FastAPI(
    title="PinSphere API",
    description="PinSphere API (version api/v1)",
    lifespan=lifespan,
)


app.include_router(api.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CorrelationIdMiddleware)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


add_exception_handler(app)
add_pagination(app)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
