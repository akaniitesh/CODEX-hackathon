from __future__ import annotations

from typing import Generic, TypeVar

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """Small async repository base for shared persistence helpers."""

    model: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, instance: ModelT) -> ModelT:
        """Add an instance and flush it to obtain generated fields."""
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def get(self, entity_id: str) -> ModelT | None:
        """Fetch an entity by primary key."""
        return await self.session.get(self.model, entity_id)

    async def paginate(
        self,
        query: Select[tuple[ModelT]],
        limit: int,
        offset: int,
    ) -> tuple[list[ModelT], int]:
        """Return a paginated result set and total count."""
        total = await self.session.scalar(
            select(func.count()).select_from(query.subquery())
        )
        result = await self.session.scalars(query.limit(limit).offset(offset))
        return list(result.all()), int(total or 0)
