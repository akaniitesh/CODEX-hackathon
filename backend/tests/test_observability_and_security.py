from __future__ import annotations

import pytest
from httpx import AsyncClient

from app.core.audit import AuditLogger
from app.core.config import Settings
from app.core.errors import ApiError
from app.core.sanitizer import sanitize_dict, sanitize_text
from app.core.security import Role, create_access_token
from app.core.security_hardening import RateLimiter


def auth_headers(settings: Settings, role: Role = Role.ADMIN) -> dict[str, str]:
    """Build authorization headers for protected observability endpoints."""
    token = create_access_token("observability-user", role, settings)
    return {"Authorization": f"Bearer {token}"}


def test_secret_sanitizer_masks_credentials() -> None:
    """Sanitizer redacts API keys, GitHub tokens, and sensitive dictionary keys."""
    raw_text = (
        "Connecting with token ghp_1234567890abcdef1234567890abcdef1234 "
        "and Bearer eyJhbGciOiJIUzI1NiJ9.test.sig"
    )
    clean_text = sanitize_text(raw_text)
    assert "ghp_12345" not in clean_text
    assert "[REDACTED_SECRET]" in clean_text

    raw_dict = {
        "user": "alice",
        "api_key": "sk-proj-secret-123",
        "nested": {"password": "supersecretpassword"},
    }
    clean_dict = sanitize_dict(raw_dict)
    assert clean_dict["api_key"] == "[REDACTED_SECRET]"
    assert clean_dict["nested"]["password"] == "[REDACTED_SECRET]"


def test_rate_limiter_blocks_exceeding_clients() -> None:
    """Rate limiter allows requests under threshold and raises 429 when exceeded."""
    limiter = RateLimiter(requests_per_minute=2)
    client_ip = "192.168.1.100"

    limiter.check_rate_limit(client_ip)
    limiter.check_rate_limit(client_ip)

    with pytest.raises(ApiError) as exc_info:
        limiter.check_rate_limit(client_ip)
    assert exc_info.value.status_code == 429


def test_audit_logger_records_sanitized_operations() -> None:
    """Audit logger appends traceable records with sanitized metadata."""
    logger = AuditLogger()
    record = logger.log(
        user_id="user-123",
        action="TRIGGER_RUN",
        resource="repo-456",
        run_id="run-789",
        metadata={"token": "sk-secret-key"},
    )

    assert record.user_id == "user-123"
    assert record.action == "TRIGGER_RUN"
    assert record.metadata["token"] == "[REDACTED_SECRET]"
    assert len(logger.records) == 1


@pytest.mark.asyncio
async def test_telemetry_health_endpoint(async_client: AsyncClient) -> None:
    """GET /api/v1/telemetry/health rejects unauthenticated callers."""
    res = await async_client.get("/api/v1/telemetry/health")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_telemetry_health_endpoint_with_admin(
    async_client: AsyncClient,
    test_settings: Settings,
) -> None:
    """Authenticated admins can read aggregated telemetry and provider status."""
    res = await async_client.get(
        "/api/v1/telemetry/health",
        headers=auth_headers(test_settings),
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "providers" in data
    assert "telemetry" in data


@pytest.mark.asyncio
async def test_prometheus_metrics_endpoint_requires_admin(
    async_client: AsyncClient,
    test_settings: Settings,
) -> None:
    """GET /api/v1/metrics/prometheus returns Prometheus plaintext format."""
    res = await async_client.get("/api/v1/metrics/prometheus")
    assert res.status_code == 401

    res = await async_client.get(
        "/api/v1/metrics/prometheus",
        headers=auth_headers(test_settings),
    )
    assert res.status_code == 200
    assert "text/plain" in res.headers["content-type"]
    assert "# HELP" in res.text
