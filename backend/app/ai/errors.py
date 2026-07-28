from __future__ import annotations


class AIProviderError(Exception):
    """Base class for provider failures."""

    retryable = False

    def __init__(self, message: str, provider: str | None = None) -> None:
        self.provider = provider
        super().__init__(message)


class RetryableAIProviderError(AIProviderError):
    """Failure that may succeed after retry or fallback."""

    retryable = True


class TerminalAIProviderError(AIProviderError):
    """Failure that must not be retried blindly."""


class RateLimitError(RetryableAIProviderError):
    """Provider returned a rate-limit response."""


class ProviderTimeoutError(RetryableAIProviderError):
    """Provider request timed out."""


class ProviderNetworkError(RetryableAIProviderError):
    """Provider request failed due to network I/O."""


class ProviderServerError(RetryableAIProviderError):
    """Provider returned a 5xx response."""


class ProviderResponseError(TerminalAIProviderError):
    """Provider returned malformed or unusable data."""


class CircuitBreakerOpenError(RetryableAIProviderError):
    """Provider circuit breaker is open."""


class TokenBudgetExceededError(TerminalAIProviderError):
    """Token or cost budget has been exceeded."""


class FallbackExhaustedError(RetryableAIProviderError):
    """All providers failed and the request was sent to retry queue."""

