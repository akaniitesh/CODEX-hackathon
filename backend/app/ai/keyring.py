from __future__ import annotations

from itertools import cycle


class ApiKeyRing:
    """Round-robin API key selector for provider key rotation."""

    def __init__(self, keys: list[str]) -> None:
        clean_keys = [key.strip() for key in keys if key.strip()]
        self._keys = clean_keys
        self._cycle = cycle(clean_keys) if clean_keys else None

    def next_key(self) -> str | None:
        """Return the next configured API key."""
        if self._cycle is None:
            return None
        return next(self._cycle)

