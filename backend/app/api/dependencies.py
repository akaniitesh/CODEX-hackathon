from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.db.session import get_db_session
from app.services.auth_service import AuthService
from app.services.repository_service import RepositoryService
from app.services.run_service import RunService
from app.services.webhook_service import GitHubWebhookService


async def get_auth_service(
    session: AsyncSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings),
) -> AuthService:
    """Provide the authentication service."""
    return AuthService(session, settings)


async def get_repository_service(
    session: AsyncSession = Depends(get_db_session),
) -> RepositoryService:
    """Provide the repository service."""
    return RepositoryService(session)


async def get_run_service(
    session: AsyncSession = Depends(get_db_session),
) -> RunService:
    """Provide the run service."""
    return RunService(session)


async def get_webhook_service(
    session: AsyncSession = Depends(get_db_session),
) -> GitHubWebhookService:
    """Provide the GitHub webhook service."""
    return GitHubWebhookService(session)

