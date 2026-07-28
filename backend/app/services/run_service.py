from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.run_repository import RunRepository
from app.schemas.common import Page
from app.schemas.run import RunRead


class RunService:
    """Business operations for runs."""

    def __init__(self, session: AsyncSession) -> None:
        self.runs = RunRepository(session)

    async def list_by_repository(
        self,
        repository_id: str,
        limit: int,
        offset: int,
    ) -> Page[RunRead]:
        """List repository runs as a paginated API page."""
        items, total = await self.runs.list_by_repository(repository_id, limit, offset)
        return Page[RunRead](
            items=[RunRead.model_validate(item) for item in items],
            total=total,
            limit=limit,
            offset=offset,
        )

