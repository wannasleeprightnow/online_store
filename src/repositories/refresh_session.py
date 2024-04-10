from typing import Optional
from uuid import UUID

from sqlalchemy import delete, select, update

from database.database import async_session_maker
from models.refresh_session import RefreshSessionModel
from utils.repository import Repository


class RefreshSessionRepository(Repository):
    model = RefreshSessionModel

    async def get_session_by_token(
        self, token: UUID
    ) -> Optional[RefreshSessionModel]:
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.token == token)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def update_session_by_id(
        self,
        new_token: UUID,
        user_id: UUID,
    ) -> RefreshSessionModel:
        async with async_session_maker() as session:
            stmt = (
                update(self.model)
                .where(self.model.user_id == user_id)
                .values(**{"token": new_token})
                .returning(self.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    async def delete_session_by_id(self, id: UUID) -> None:
        async with async_session_maker() as session:
            stmt = delete(self.model).where(self.model.id == id)
            await session.execute(stmt)
            await session.commit()

    async def delete_session_by_token(self, token: UUID) -> None:
        async with async_session_maker() as session:
            stmt = delete(self.model).where(self.model.token == token)
            await session.execute(stmt)
            await session.commit()

    async def delete_all_sessions_by_user_id(self, user_id: UUID) -> None:
        async with async_session_maker() as session:
            stmt = delete(self.model).where(self.model.user_id == user_id)
            await session.execute(stmt)
            await session.commit()

    async def get_session_by_user_id(
        self, user_id: UUID
    ) -> Optional[list[RefreshSessionModel]]:
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.user_id == user_id)
            result = await session.execute(stmt)
            return result.scalars().all()
