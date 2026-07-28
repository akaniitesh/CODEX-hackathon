from __future__ import annotations

import hashlib
import hmac
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any

import jwt
from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext

from app.core.config import Settings, get_settings
from app.core.errors import ApiError


class Role(StrEnum):
    """Supported organization roles."""

    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


ROLE_ORDER = {
    Role.VIEWER: 0,
    Role.MEMBER: 1,
    Role.ADMIN: 2,
    Role.OWNER: 3,
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer(auto_error=False)


def create_access_token(
    subject: str,
    role: Role,
    settings: Settings,
) -> str:
    """Create a signed JWT access token."""
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.jwt_expire_minutes)
    payload: dict[str, Any] = {
        "sub": subject,
        "role": role.value,
        "exp": expires_at,
        "iat": datetime.now(UTC),
    }
    return jwt.encode(
        payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def decode_access_token(token: str, settings: Settings) -> dict[str, Any]:
    """Decode and validate a JWT access token."""
    try:
        return jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.PyJWTError as exc:
        raise ApiError(
            "Invalid authentication token.", status.HTTP_401_UNAUTHORIZED
        ) from exc


async def get_current_claims(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    settings: Settings = Depends(get_settings),
) -> dict[str, Any]:
    """Extract current JWT claims from the authorization header."""
    if credentials is None:
        raise ApiError("Authentication required.", status.HTTP_401_UNAUTHORIZED)
    return decode_access_token(credentials.credentials, settings)


def require_role(minimum_role: Role) -> Any:
    """Build a dependency requiring at least the supplied role."""

    async def dependency(
        claims: dict[str, Any] = Depends(get_current_claims),
    ) -> dict[str, Any]:
        role = Role(claims.get("role", Role.VIEWER))
        if ROLE_ORDER[role] < ROLE_ORDER[minimum_role]:
            raise ApiError("Insufficient permissions.", status.HTTP_403_FORBIDDEN)
        return claims

    return dependency


def verify_github_signature(
    body: bytes,
    signature_header: str | None,
    settings: Settings,
) -> None:
    """Verify a GitHub webhook HMAC before payload parsing."""
    if not settings.github_webhook_secret:
        raise ApiError(
            "Webhook secret is not configured.", status.HTTP_503_SERVICE_UNAVAILABLE
        )
    if not signature_header or not signature_header.startswith("sha256="):
        raise ApiError("Missing GitHub signature.", status.HTTP_401_UNAUTHORIZED)
    digest = hmac.new(
        settings.github_webhook_secret.encode("utf-8"),
        body,
        hashlib.sha256,
    ).hexdigest()
    expected = f"sha256={digest}"
    if not hmac.compare_digest(expected, signature_header):
        raise ApiError("Invalid GitHub signature.", status.HTTP_401_UNAUTHORIZED)
