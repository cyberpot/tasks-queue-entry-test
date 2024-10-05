from abc import ABC
import typing

from sqlalchemy import select, exists, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import BaseModel


ModelT = typing.TypeVar("ModelT", bound=BaseModel)


class InstanceDoesNotExist(Exception):
    ...


class SQLAlchemyBaseModelManager(ABC, typing.Generic[ModelT]):
    model: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: dict | None) -> ModelT:
        process = self.model(**data) if data else self.model()
        self.session.add(process)
        await self.session.flush()
        return process

    async def bulk_remove(self, ids: list[str]):
        await self.session.execute(
            delete(self.model)
            .where(self.model.id.in_(ids))
        )

    async def get_by_id(self, instance_id: str) -> ModelT | None:
        return await self.session.get(self.model, instance_id)

    async def update(self, instance_id: str, data: dict | None) -> None:
        await self.session.execute(
            update(self.model)
            .where(self.model.id == instance_id)
            .values(**data)
        )
