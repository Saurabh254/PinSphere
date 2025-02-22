from logging_conf import log

import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from pin_sphere import api
from pin_sphere.exception_handling import add_exception_handler

app = FastAPI(
    debug=True,
    title="PinSphere API",
    description="PinSphere API (version api/v1)",
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
add_exception_handler(app)
add_pagination(app)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
