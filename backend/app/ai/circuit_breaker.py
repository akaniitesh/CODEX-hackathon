from __future__ import annotations

from collections.abc import Awaitable, Callable
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import TypeVar

from app.ai.errors import CircuitBreakerOpenError, RetryableAIProviderError
from app.ai.schemas import ProviderName

ResultT = TypeVar("ResultT")


class CircuitState(StrEnum):
    """Circuit breaker states."""

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    """Explicit circuit breaker state machine for one provider."""

    def __init__(
        self,
        provider: ProviderName,
        failure_threshold: int,
        cooldown_seconds: float,
    ) -> None:
        self.provider = provider
        self.failure_threshold = failure_threshold
        self.cooldown = timedelta(seconds=cooldown_seconds)
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.opened_at: datetime | None = None

    async def call(self, operation: Callable[[], Awaitable[ResultT]]) -> ResultT:
        """Run an operation if the circuit allows it."""
        self._transition_before_call()
        try:
            result = await operation()
        except RetryableAIProviderError:
            self.record_failure()
            raise
        self.record_success()
        return result

    def record_failure(self) -> None:
        """Record a provider failure and open the circuit at threshold."""
        self.failure_count += 1
        if self.state == CircuitState.HALF_OPEN:
            self._open()
            return
        if self.failure_count >= self.failure_threshold:
            self._open()

    def record_success(self) -> None:
        """Close the circuit after a successful call."""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.opened_at = None

    def _transition_before_call(self) -> None:
        """Move open circuits into half-open after cooldown."""
        if self.state != CircuitState.OPEN:
            return
        if self.opened_at and datetime.now(UTC) - self.opened_at >= self.cooldown:
            self.state = CircuitState.HALF_OPEN
            return
        raise CircuitBreakerOpenError("Circuit breaker is open.", self.provider)

    def _open(self) -> None:
        """Trip the circuit open."""
        self.state = CircuitState.OPEN
        self.opened_at = datetime.now(UTC)

