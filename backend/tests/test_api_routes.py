from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.core.security import Role, create_access_token
from app.models.organization import Organization
from app.models.repository import Repository
from app.models.run import Run


@pytest.mark.asyncio
async def test_health_endpoints(async_client: AsyncClient) -> None:
    """Process health and database health endpoints return status ok."""
    res1 = await async_client.get("/api/v1/health")
    assert res1.status_code == 200
    assert res1.json() == {"status": "ok"}
    assert res1.headers["x-content-type-options"] == "nosniff"

    res2 = await async_client.get("/api/v1/health/db")
    assert res2.status_code == 200
    assert res2.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_repositories_endpoint_requires_auth(
    async_client: AsyncClient,
) -> None:
    """Listing repositories without JWT returns 401 Unauthorized."""
    res = await async_client.get("/api/v1/repositories")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_repositories_endpoint_success(
    async_client: AsyncClient,
    db_session: AsyncSession,
    test_settings: Settings,
) -> None:
    """Authenticated request returns paginated active repositories."""
    org = Organization(name="Gamma Ltd", slug="gamma")
    db_session.add(org)
    await db_session.flush()

    repo = Repository(
        organization_id=org.id,
        github_repo_id="99999",
        owner="gamma",
        name="gamma-repo",
        clone_url="https://github.com/gamma/gamma-repo.git",
        default_branch="main",
    )
    db_session.add(repo)
    await db_session.commit()

    token = create_access_token("user-viewer", Role.VIEWER, test_settings)
    headers = {"Authorization": f"Bearer {token}"}

    res = await async_client.get("/api/v1/repositories", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "gamma-repo"
    assert data["items"][0]["owner"] == "gamma"


@pytest.mark.asyncio
async def test_repository_runs_endpoint_success(
    async_client: AsyncClient,
    db_session: AsyncSession,
    test_settings: Settings,
) -> None:
    """Authenticated request returns paginated runs for a specific repository."""
    org = Organization(name="Delta LLC", slug="delta")
    db_session.add(org)
    await db_session.flush()

    repo = Repository(
        organization_id=org.id,
        github_repo_id="88888",
        owner="delta",
        name="delta-repo",
        clone_url="https://github.com/delta/delta-repo.git",
        default_branch="main",
    )
    db_session.add(repo)
    await db_session.flush()

    run = Run(
        repository_id=repo.id,
        event_type="push",
        commit_sha="abcdef1234567890",
        branch="main",
        status="pending",
        webhook_delivery_id="deliv-100",
    )
    db_session.add(run)
    await db_session.commit()

    token = create_access_token("user-member", Role.MEMBER, test_settings)
    headers = {"Authorization": f"Bearer {token}"}

    url = f"/api/v1/runs/repositories/{repo.id}"
    res = await async_client.get(url, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["commit_sha"] == "abcdef1234567890"
    assert data["items"][0]["status"] == "pending"
