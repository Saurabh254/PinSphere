import uvicorn
from starlette.middleware.cors import CORSMiddleware

from pin_sphere import api
from fastapi import FastAPI

from pin_sphere.exception_handling import add_exception_handler

from asgi_correlation_id import CorrelationIdMiddleware

app = FastAPI(
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
