from __future__ import annotations

import pytest
from httpx import AsyncClient

from app.core.config import Settings
from app.core.errors import ApiError
from app.core.security import (
    Role,
    create_access_token,
    decode_access_token,
)


def test_jwt_create_and_decode(test_settings: Settings) -> None:
    """JWT token can be created and decoded with matching claims."""
    token = create_access_token("user-123", Role.ADMIN, test_settings)
    claims = decode_access_token(token, test_settings)
    assert claims["sub"] == "user-123"
    assert claims["role"] == "admin"


def test_jwt_decode_invalid(test_settings: Settings) -> None:
    """Invalid token raises 401 ApiError."""
    with pytest.raises(ApiError) as exc_info:
        decode_access_token("invalid.token.str", test_settings)
    assert exc_info.value.status_code == 401


def test_settings_accepts_legacy_secret_env_names(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Settings accept legacy env names documented before the security cleanup."""
    monkeypatch.setenv("SECRET_KEY", "legacy-jwt-secret-key-at-least-32-bytes")
    monkeypatch.setenv("WEBHOOK_SECRET", "legacy-webhook-secret")

    settings = Settings()

    assert settings.jwt_secret_key == "legacy-jwt-secret-key-at-least-32-bytes"
    assert settings.github_webhook_secret == "legacy-webhook-secret"


def test_production_settings_reject_insecure_defaults() -> None:
    """Production configuration rejects insecure JWT and CORS defaults."""
    with pytest.raises(ValueError, match="JWT_SECRET_KEY"):
        Settings(
            environment="production",
            jwt_secret_key="dev-only-change-me",
            github_webhook_secret="webhook-secret",
            cors_origins=["http://localhost"],
        )


@pytest.mark.asyncio
async def test_auth_github_start(
    async_client: AsyncClient,
    test_settings: Settings,
) -> None:
    """GitHub OAuth start route returns valid auth URL."""
    response = await async_client.get("/api/v1/auth/github/start?state=test-state")
    assert response.status_code == 200
    data = response.json()
    assert "authorization_url" in data
    assert "github.com/login/oauth/authorize" in data["authorization_url"]
