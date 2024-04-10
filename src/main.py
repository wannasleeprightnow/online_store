import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import apiv1
from settings import AppSettings

app = FastAPI(title="online_store")
logger = logging.getLogger(__name__)

app.include_router(apiv1)
app.add_middleware(
    CORSMiddleware,
    allow_origins=AppSettings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
