from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.repository_repository import RepositoryRepository
from app.schemas.common import Page
from app.schemas.repository import RepositoryRead


class RepositoryService:
    """Business operations for connected repositories."""

    def __init__(self, session: AsyncSession) -> None:
        self.repositories = RepositoryRepository(session)

    async def list_active(self, limit: int, offset: int) -> Page[RepositoryRead]:
        """List active repositories as a paginated API page."""
        items, total = await self.repositories.list_active(limit, offset)
        return Page[RepositoryRead](
            items=[RepositoryRead.model_validate(item) for item in items],
            total=total,
            limit=limit,
            offset=offset,
        )

