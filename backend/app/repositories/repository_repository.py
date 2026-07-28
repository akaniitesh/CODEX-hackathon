from __future__ import annotations

from sqlalchemy import select

from app.models.repository import Repository
from app.repositories.base import BaseRepository


class RepositoryRepository(BaseRepository[Repository]):
    """Persistence operations for connected repositories."""

    model = Repository

    async def list_active(
        self, limit: int, offset: int
    ) -> tuple[list[Repository], int]:
        """List active repositories with pagination."""
        query = select(Repository).where(Repository.is_active.is_(True))
        return await self.paginate(query, limit, offset)

    async def get_by_github_id(self, github_repo_id: str) -> Repository | None:
        """Find a repository by GitHub repository id."""
        result = await self.session.scalars(
            select(Repository).where(Repository.github_repo_id == github_repo_id)
        )
        return result.first()

    async def get_by_full_name(self, full_name: str) -> Repository | None:
        """Find a repository by owner/name."""
        if "/" not in full_name:
            return None
        owner, name = full_name.split("/", 1)
        result = await self.session.scalars(
            select(Repository).where(
                Repository.owner == owner,
                Repository.name == name,
            )
        )
        return result.first()

