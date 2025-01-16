from starlette.middleware.cors import CORSMiddleware

from pin_sphere import api
from fastapi import FastAPI

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
