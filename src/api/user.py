from fastapi import APIRouter, Depends

from api.dependencies import user_service
from services.user import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/user")
async def users_list(service: UserService = Depends(user_service)):
    return await service.get_all_users()
