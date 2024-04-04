from models.user import UserModel
from repositories.user import UserRepository
from schemas.user import UserRegister


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository: UserRepository = user_repository()

    async def get_all_users(self) -> list[UserModel]:
        return await self.user_repository.get_all()

    async def is_user_exists(self, user: UserRegister) -> bool:
        ...
