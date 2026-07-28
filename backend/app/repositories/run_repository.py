from __future__ import annotations

from sqlalchemy import select

from app.models.run import Run
from app.repositories.base import BaseRepository


class RunRepository(BaseRepository[Run]):
    """Persistence operations for runs."""

    model = Run

    async def list_by_repository(
        self,
        repository_id: str,
        limit: int,
        offset: int,
    ) -> tuple[list[Run], int]:
        """List runs for a repository with newest first ordering."""
        query = (
            select(Run)
            .where(Run.repository_id == repository_id)
            .order_by(Run.created_at.desc())
        )
        return await self.paginate(query, limit, offset)

    async def find_duplicate(
        self,
        repository_id: str,
        commit_sha: str,
        event_type: str,
        delivery_id: str | None,
    ) -> Run | None:
        """Find an existing run for a delivery or repo/commit/event tuple."""
        if delivery_id:
            by_delivery = await self.session.scalars(
                select(Run).where(Run.webhook_delivery_id == delivery_id)
            )
            existing = by_delivery.first()
            if existing is not None:
                return existing
        result = await self.session.scalars(
            select(Run).where(
                Run.repository_id == repository_id,
                Run.commit_sha == commit_sha,
                Run.event_type == event_type,
            )
        )
        return result.first()

