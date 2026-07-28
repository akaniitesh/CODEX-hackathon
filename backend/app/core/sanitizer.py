from __future__ import annotations

import re
from typing import Any

SECRET_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"ghp_[A-Za-z0-9]{36}"),
    re.compile(r"sk-[A-Za-z0-9]{32,64}"),
    re.compile(r"gsk_[A-Za-z0-9]{32,64}"),
    re.compile(r"Bearer\s+[A-Za-z0-9\-\._~\+\/]+=*", re.IGNORECASE),
    re.compile(r"eyJ[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+"),
    re.compile(
        r"(?:password|secret|api_key|token|private_key)\s*[:=]\s*['\"]?([^\s'\"]+)['\"]?",
        re.IGNORECASE,
    ),
]

SENSITIVE_KEY_NAMES: set[str] = {
    "password",
    "secret",
    "api_key",
    "token",
    "access_token",
    "private_key",
    "webhook_secret",
    "github_token",
    "jwt_secret",
}


def sanitize_text(text: str) -> str:
    """Sanitize sensitive credentials, tokens, and keys from raw text string."""
    sanitized = text
    for pattern in SECRET_PATTERNS:
        sanitized = pattern.sub("[REDACTED_SECRET]", sanitized)
    return sanitized


def sanitize_dict(data: dict[str, Any]) -> dict[str, Any]:
    """Recursively sanitize sensitive key values inside dictionaries."""
    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in SENSITIVE_KEY_NAMES:
            sanitized[key] = "[REDACTED_SECRET]"
        elif isinstance(value, dict):
            sanitized[key] = sanitize_dict(value)
        elif isinstance(value, list):
            sanitized[key] = [
                sanitize_dict(item) if isinstance(item, dict)
                else (sanitize_text(item) if isinstance(item, str) else item)
                for item in value
            ]
        elif isinstance(value, str):
            sanitized[key] = sanitize_text(value)
        else:
            sanitized[key] = value
    return sanitized
