from abc import ABC, abstractmethod
from typing import Iterable

from sqlalchemy import insert, select

from database.database import async_session_maker, Base


class AbstractRepository(ABC):

    @abstractmethod
    async def get_all(self) -> Iterable:
        ...

    @abstractmethod
    async def insert_one(self, _) -> Base:
        ...


class Repository(AbstractRepository):
    model = Base

    async def get_all(self) -> Iterable:
        async with async_session_maker() as session:
            query = select(self.model)
            result = await session.execute(query)
            return result.scalars().all()

    async def insert_one(self, model_dump: dict) -> model:
        async with async_session_maker() as session:
            stmt = (
                insert(self.model).values(**model_dump).returning(self.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()
