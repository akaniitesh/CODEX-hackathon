from __future__ import annotations

import hashlib
import hmac
import json
from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.core.errors import ApiError
from app.core.security import verify_github_signature
from app.models.organization import Organization
from app.models.repository import Repository


def compute_signature(secret: str, body: bytes) -> str:
    """Compute GitHub HMAC SHA256 signature header."""
    digest = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def test_verify_github_signature_valid(test_settings: Settings) -> None:
    """Valid HMAC signature passes verification without error."""
    body = b'{"ref": "refs/heads/main"}'
    signature = compute_signature(test_settings.github_webhook_secret, body)
    verify_github_signature(body, signature, test_settings)


def test_verify_github_signature_invalid(test_settings: Settings) -> None:
    """Invalid HMAC signature raises 401 ApiError."""
    body = b'{"ref": "refs/heads/main"}'
    with pytest.raises(ApiError) as exc_info:
        verify_github_signature(body, "sha256=invaliddigest", test_settings)
    assert exc_info.value.status_code == 401


def test_verify_github_signature_missing_header(test_settings: Settings) -> None:
    """Missing signature header raises 401 ApiError."""
    body = b'{"ref": "refs/heads/main"}'
    with pytest.raises(ApiError) as exc_info:
        verify_github_signature(body, None, test_settings)
    assert exc_info.value.status_code == 401


def test_verify_github_signature_unconfigured_secret() -> None:
    """Unconfigured webhook secret raises 503 ApiError."""
    settings = Settings(github_webhook_secret="")
    body = b'{"ref": "refs/heads/main"}'
    with pytest.raises(ApiError) as exc_info:
        verify_github_signature(body, "sha256=somehash", settings)
    assert exc_info.value.status_code == 503


@pytest.mark.asyncio
async def test_webhook_endpoint_enqueues_run_for_connected_repo(
    async_client: AsyncClient,
    db_session: AsyncSession,
    test_settings: Settings,
) -> None:
    """Valid webhook payload for a registered repository enqueues a run."""
    org = Organization(name="Acme Corp", slug="acme")
    db_session.add(org)
    await db_session.flush()

    repo = Repository(
        organization_id=org.id,
        github_repo_id="12345",
        owner="acme",
        name="demo-repo",
        clone_url="https://github.com/acme/demo-repo.git",
        default_branch="main",
    )
    db_session.add(repo)
    await db_session.commit()

    payload = {
        "ref": "refs/heads/main",
        "after": "abc1234567890def",
        "repository": {"full_name": "acme/demo-repo"},
        "head_commit": {"id": "abc1234567890def"},
    }
    body = json.dumps(payload).encode("utf-8")
    signature = compute_signature(test_settings.github_webhook_secret, body)

    headers = {
        "X-GitHub-Event": "push",
        "X-GitHub-Delivery": "delivery-uuid-001",
        "X-Hub-Signature-256": signature,
        "Content-Type": "application/json",
    }

    with patch("app.services.webhook_service.enqueue_run.delay") as mock_delay:
        response = await async_client.post(
            "/api/v1/webhooks/github",
            content=body,
            headers=headers,
        )

    assert response.status_code == 200
    data = response.json()
    assert data["accepted"] is True
    assert data["duplicate"] is False
    assert data["run_id"] is not None
    mock_delay.assert_called_once_with(data["run_id"])


@pytest.mark.asyncio
async def test_webhook_endpoint_deduplicates_delivery_id(
    async_client: AsyncClient,
    db_session: AsyncSession,
    test_settings: Settings,
) -> None:
    """Duplicate X-GitHub-Delivery IDs return duplicate=True without re-enqueuing."""
    org = Organization(name="Beta Inc", slug="beta")
    db_session.add(org)
    await db_session.flush()

    repo = Repository(
        organization_id=org.id,
        github_repo_id="67890",
        owner="beta",
        name="beta-repo",
        clone_url="https://github.com/beta/beta-repo.git",
        default_branch="main",
    )
    db_session.add(repo)
    await db_session.commit()

    payload = {
        "ref": "refs/heads/main",
        "after": "def9876543210abc",
        "repository": {"full_name": "beta/beta-repo"},
        "head_commit": {"id": "def9876543210abc"},
    }
    body = json.dumps(payload).encode("utf-8")
    signature = compute_signature(test_settings.github_webhook_secret, body)

    headers = {
        "X-GitHub-Event": "push",
        "X-GitHub-Delivery": "delivery-uuid-dup",
        "X-Hub-Signature-256": signature,
        "Content-Type": "application/json",
    }

    with patch("app.services.webhook_service.enqueue_run.delay"):
        res1 = await async_client.post(
            "/api/v1/webhooks/github", content=body, headers=headers
        )
        assert res1.status_code == 200
        assert res1.json()["accepted"] is True
        assert res1.json()["duplicate"] is False

        res2 = await async_client.post(
            "/api/v1/webhooks/github", content=body, headers=headers
        )
        assert res2.status_code == 200
        assert res2.json()["accepted"] is True
        assert res2.json()["duplicate"] is True


@pytest.mark.asyncio
async def test_webhook_endpoint_ignores_unconnected_repo(
    async_client: AsyncClient,
    test_settings: Settings,
) -> None:
    """Webhooks for repos not registered in the system are safely ignored."""
    payload = {
        "ref": "refs/heads/main",
        "after": "1112223334445556",
        "repository": {"full_name": "unknown/unconnected-repo"},
    }
    body = json.dumps(payload).encode("utf-8")
    signature = compute_signature(test_settings.github_webhook_secret, body)

    headers = {
        "X-GitHub-Event": "push",
        "X-GitHub-Delivery": "delivery-uuid-unconnected",
        "X-Hub-Signature-256": signature,
        "Content-Type": "application/json",
    }

    response = await async_client.post(
        "/api/v1/webhooks/github", content=body, headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["accepted"] is False
    assert data["duplicate"] is False
