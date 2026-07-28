from __future__ import annotations

from pathlib import Path

SENSITIVE_FILENAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "id_rsa",
    "id_dsa",
    "id_ed25519",
    "credentials",
    "credentials.json",
}

SENSITIVE_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}


def is_sensitive_path(path: Path) -> bool:
    """Return whether a repository path should never be read into memory."""
    lowered = path.name.lower()
    return lowered in SENSITIVE_FILENAMES or path.suffix.lower() in SENSITIVE_SUFFIXES


def safe_relative_path(root: Path, path: Path) -> str:
    """Return a normalized repo-relative path after containment validation."""
    resolved_root = root.resolve()
    resolved_path = path.resolve()
    if resolved_root not in resolved_path.parents and resolved_path != resolved_root:
        raise ValueError("Path escapes repository root.")
    return resolved_path.relative_to(resolved_root).as_posix()

