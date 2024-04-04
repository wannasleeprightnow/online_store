from fastapi import APIRouter

from api.auth import router as auth_router
from api.user import router as user_router
from settings import AppSettings

all_routers = [auth_router, user_router]

apiv1 = APIRouter(prefix=AppSettings.api_v1_prefix)

for router in all_routers:
    apiv1.include_router(router)
