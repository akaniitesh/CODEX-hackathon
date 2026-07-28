from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_run_service
from app.core.security import Role, require_role
from app.schemas.common import Page
from app.schemas.run import RunRead
from app.services.run_service import RunService

router = APIRouter()


@router.get("/repositories/{repository_id}", response_model=Page[RunRead])
async def list_repository_runs(
    repository_id: str,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    _claims: dict[str, object] = Depends(require_role(Role.VIEWER)),
    service: RunService = Depends(get_run_service),
) -> Page[RunRead]:
    """List runs for a repository."""
    return await service.list_by_repository(repository_id, limit, offset)

