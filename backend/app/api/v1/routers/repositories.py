from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_repository_service
from app.core.security import Role, require_role
from app.schemas.common import Page
from app.schemas.repository import RepositoryRead
from app.services.repository_service import RepositoryService

router = APIRouter()


@router.get("", response_model=Page[RepositoryRead])
async def list_repositories(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    _claims: dict[str, object] = Depends(require_role(Role.VIEWER)),
    service: RepositoryService = Depends(get_repository_service),
) -> Page[RepositoryRead]:
    """List active repositories."""
    return await service.list_active(limit, offset)

