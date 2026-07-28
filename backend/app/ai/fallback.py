from __future__ import annotations

from collections.abc import AsyncIterator
from typing import TypeVar

from pydantic import BaseModel

from app.ai.base import BaseAIProvider
from app.ai.budget import TokenBudgetManager
from app.ai.circuit_breaker import CircuitBreaker
from app.ai.errors import (
    AIProviderError,
    FallbackExhaustedError,
    TokenBudgetExceededError,
)
from app.ai.retry import RetryPolicy
from app.ai.retry_queue import InMemoryRetryQueue
from app.ai.schemas import AIRequest, AIResponse, ProviderName, StreamChunk
from app.ai.structured import parse_json_with_retry

StructuredT = TypeVar("StructuredT", bound=BaseModel)


class FallbackAIProvider(BaseAIProvider):
    """Provider wrapper with retry, fallback, circuit, and budget controls."""

    name = ProviderName.GROQ

    def __init__(
        self,
        providers: list[BaseAIProvider],
        breakers: dict[ProviderName, CircuitBreaker],
        retry_policy: RetryPolicy,
        retry_queue: InMemoryRetryQueue,
        budget_manager: TokenBudgetManager,
    ) -> None:
        self.providers = providers
        self.breakers = breakers
        self.retry_policy = retry_policy
        self.retry_queue = retry_queue
        self.budget_manager = budget_manager

    async def generate(self, request: AIRequest) -> AIResponse:
        """Generate with provider fallback and explicit retry queue exhaustion."""
        self.budget_manager.ensure_allowed(request.run_id, request.user_id)
        self.budget_manager.reserve(request.run_id, request.user_id, request.max_tokens)
        errors: list[str] = []
        for provider in self.providers:
            try:
                response = await self._call_provider(provider, request)
                self.budget_manager.record_usage(
                    request.run_id,
                    request.user_id,
                    response.usage,
                )
                return response
            except TokenBudgetExceededError:
                raise
            except AIProviderError as exc:
                errors.append(f"{provider.name}: {type(exc).__name__}")
                continue
        await self.retry_queue.enqueue(request, errors)
        raise FallbackExhaustedError("All AI providers failed; request queued.")

    async def stream(self, request: AIRequest) -> AsyncIterator[StreamChunk]:
        """Stream using the first available provider in fallback order."""
        self.budget_manager.ensure_allowed(request.run_id, request.user_id)
        self.budget_manager.reserve(request.run_id, request.user_id, request.max_tokens)
        errors: list[str] = []
        for provider in self.providers:
            try:
                target_provider = provider
                breaker = self.breakers[target_provider.name]

                async def start_stream(
                    p: BaseAIProvider = target_provider,
                ) -> AsyncIterator[StreamChunk]:
                    return p.stream(request)

                stream_result = await breaker.call(start_stream)
                async for chunk in stream_result:
                    yield chunk
                return
            except TokenBudgetExceededError:
                raise
            except AIProviderError as exc:
                errors.append(f"{provider.name}: {type(exc).__name__}")
                continue
        await self.retry_queue.enqueue(request, errors)
        raise FallbackExhaustedError("All AI providers failed; request queued.")

    async def structured_output(
        self,
        request: AIRequest,
        schema: type[StructuredT],
    ) -> StructuredT:
        """Generate structured output with JSON parse retry."""
        return await parse_json_with_retry(self, request, schema)

    async def _call_provider(
        self,
        provider: BaseAIProvider,
        request: AIRequest,
    ) -> AIResponse:
        """Call one provider through its breaker and retry policy."""
        breaker = self.breakers[provider.name]

        async def operation() -> AIResponse:
            return await provider.generate(request)

        return await breaker.call(lambda: self.retry_policy.run(operation))
