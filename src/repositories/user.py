from typing import Optional
from uuid import UUID

from sqlalchemy import select

from database.database import async_session_maker
from models.user import UserModel
from utils.repository import Repository


class UserRepository(Repository):
    model = UserModel

    async def get_one_by_username(self, username: str) -> Optional[UserModel]:
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.username == username)
            result = await session.execute(query)
            return result.scalars().one_or_none()

    async def get_one_by_user_id(self, user_id: UUID) -> Optional[UserModel]:
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.id == user_id)
            result = await session.execute(query)
            return result.scalars().one_or_none()
