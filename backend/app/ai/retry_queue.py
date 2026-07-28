from __future__ import annotations

from dataclasses import dataclass, field

from app.ai.schemas import AIRequest


@dataclass
class RetryQueueItem:
    """Request record sent to the AI retry queue after fallback exhaustion."""

    request: AIRequest
    errors: list[str] = field(default_factory=list)


class InMemoryRetryQueue:
    """Minimal retry queue abstraction for Phase 3 tests."""

    def __init__(self) -> None:
        self.items: list[RetryQueueItem] = []

    async def enqueue(self, request: AIRequest, errors: list[str]) -> None:
        """Record a request for later retry."""
        self.items.append(RetryQueueItem(request=request, errors=errors))

