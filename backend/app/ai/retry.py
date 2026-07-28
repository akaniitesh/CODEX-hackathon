from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

from app.ai.errors import AIProviderError, RetryableAIProviderError

ResultT = TypeVar("ResultT")


class RetryPolicy:
    """Exponential-backoff retry policy for retryable provider failures."""

    def __init__(self, max_attempts: int, base_delay_seconds: float) -> None:
        self.max_attempts = max_attempts
        self.base_delay_seconds = base_delay_seconds

    async def run(self, operation: Callable[[], Awaitable[ResultT]]) -> ResultT:
        """Run an async operation with exponential backoff."""
        attempt = 0
        while True:
            try:
                return await operation()
            except RetryableAIProviderError:
                attempt += 1
                if attempt >= self.max_attempts:
                    raise
                await asyncio.sleep(self.base_delay_seconds * (2 ** (attempt - 1)))
            except AIProviderError:
                raise

