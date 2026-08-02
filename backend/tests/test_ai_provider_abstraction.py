from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta

import pytest
from pydantic import BaseModel

from app.ai.base import BaseAIProvider
from app.ai.budget import TokenBudgetManager
from app.ai.circuit_breaker import CircuitBreaker, CircuitState
from app.ai.errors import (
    CircuitBreakerOpenError,
    FallbackExhaustedError,
    ProviderTimeoutError,
    RateLimitError,
    TokenBudgetExceededError,
)
from app.ai.factory import create_provider
from app.ai.fallback import FallbackAIProvider
from app.ai.retry import RetryPolicy
from app.ai.retry_queue import InMemoryRetryQueue
from app.ai.schemas import (
    AIMessage,
    AIRequest,
    AIResponse,
    ProviderName,
    StreamChunk,
    TokenUsage,
)
from app.ai.structured import parse_json_with_retry
from app.core.config import Settings


class ExampleOutput(BaseModel):
    """Structured test schema."""

    title: str
    score: int


class MockProvider(BaseAIProvider):
    """Mock provider with scripted responses and failures."""

    def __init__(self, name: ProviderName, outcomes: list[object]) -> None:
        self.name = name
        self.outcomes = outcomes
        self.calls = 0

    async def generate(self, request: AIRequest) -> AIResponse:
        """Return the next scripted outcome."""
        self.calls += 1
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome  # type: ignore[return-value]

    async def stream(self, request: AIRequest) -> AsyncIterator[StreamChunk]:
        """Yield one mocked stream chunk."""
        yield StreamChunk(provider=self.name, model="mock", delta="ok", done=True)

    async def structured_output(  # type: ignore[override]
        self,
        request: AIRequest,
        schema: type[BaseModel],
    ) -> BaseModel:
        """Validate generated content against a schema."""
        response = await self.generate(request)
        return schema.model_validate_json(response.content)


def request(max_tokens: int = 100) -> AIRequest:
    """Create a minimal provider request."""
    return AIRequest(
        messages=[AIMessage(role="user", content="Summarize this.")],
        run_id="run-1",
        user_id="user-1",
        max_tokens=max_tokens,
    )


def response(
    provider: ProviderName,
    content: str = "ok",
    tokens: int = 10,
) -> AIResponse:
    """Create a minimal provider response."""
    return AIResponse(
        provider=provider,
        model="mock",
        content=content,
        usage=TokenUsage(total_tokens=tokens),
    )


def fallback_client(
    providers: list[BaseAIProvider] | list[MockProvider],
    budget: TokenBudgetManager | None = None,
    queue: InMemoryRetryQueue | None = None,
) -> FallbackAIProvider:
    """Build a fallback client with test-friendly settings."""
    cast_providers = [p for p in providers]
    breakers = {
        provider.name: CircuitBreaker(
            provider.name, failure_threshold=2, cooldown_seconds=0
        )
        for provider in cast_providers
    }
    return FallbackAIProvider(
        providers=cast_providers,
        breakers=breakers,
        retry_policy=RetryPolicy(max_attempts=2, base_delay_seconds=0),
        retry_queue=queue or InMemoryRetryQueue(),
        budget_manager=budget
        or TokenBudgetManager(
            default_run_token_limit=1_000,
            default_user_token_limit=1_000,
            default_run_cost_limit_usd=10,
            default_user_cost_limit_usd=10,
        ),
    )


@pytest.mark.asyncio
async def test_normal_response_uses_first_provider() -> None:
    """Fallback client returns the first successful provider response."""
    groq = MockProvider(ProviderName.GROQ, [response(ProviderName.GROQ)])
    client = fallback_client([groq])

    result = await client.generate(request())

    assert result.provider == ProviderName.GROQ
    assert result.content == "ok"
    assert groq.calls == 1


@pytest.mark.asyncio
async def test_malformed_structured_response_reprompts() -> None:
    """Malformed JSON is rejected and retried with stricter instruction."""
    provider = MockProvider(
        ProviderName.OPENAI,
        [
            response(ProviderName.OPENAI, content="not json"),
            response(ProviderName.OPENAI, content='{"title":"fixed","score":5}'),
        ],
    )

    parsed = await parse_json_with_retry(provider, request(), ExampleOutput)

    assert parsed == ExampleOutput(title="fixed", score=5)
    assert provider.calls == 2


@pytest.mark.asyncio
async def test_timeout_retries_then_falls_back() -> None:
    """Timeouts are retried, then the next provider is used."""
    groq = MockProvider(
        ProviderName.GROQ,
        [
            ProviderTimeoutError("timeout", "groq"),
            ProviderTimeoutError("timeout", "groq"),
        ],
    )
    openai = MockProvider(ProviderName.OPENAI, [response(ProviderName.OPENAI)])
    client = fallback_client([groq, openai])

    result = await client.generate(request())

    assert result.provider == ProviderName.OPENAI
    assert groq.calls == 2
    assert openai.calls == 1


@pytest.mark.asyncio
async def test_rate_limit_retries_then_falls_back() -> None:
    """Rate limits are classified as retryable failures."""
    groq = MockProvider(
        ProviderName.GROQ,
        [RateLimitError("limited", "groq"), RateLimitError("limited", "groq")],
    )
    openai = MockProvider(ProviderName.OPENAI, [response(ProviderName.OPENAI)])
    client = fallback_client([groq, openai])

    result = await client.generate(request())

    assert result.provider == ProviderName.OPENAI
    assert groq.calls == 2


@pytest.mark.asyncio
async def test_full_fallback_chain_exhaustion_queues_retry() -> None:
    """All-provider failure sends the request to the retry queue."""
    queue = InMemoryRetryQueue()
    providers = [
        MockProvider(ProviderName.GROQ, [ProviderTimeoutError("t", "groq")] * 2),
        MockProvider(ProviderName.OPENAI, [ProviderTimeoutError("t", "openai")] * 2),
        MockProvider(ProviderName.OLLAMA, [ProviderTimeoutError("t", "ollama")] * 2),
    ]
    client = fallback_client(providers, queue=queue)

    with pytest.raises(FallbackExhaustedError):
        await client.generate(request())

    assert len(queue.items) == 1
    assert queue.items[0].request.run_id == "run-1"


@pytest.mark.asyncio
async def test_circuit_breaker_trip_half_open_and_close() -> None:
    """Circuit breaker opens, probes half-open, then closes on success."""
    breaker = CircuitBreaker(
        ProviderName.GROQ, failure_threshold=2, cooldown_seconds=60
    )

    async def fail() -> str:
        raise ProviderTimeoutError("timeout", "groq")

    with pytest.raises(ProviderTimeoutError):
        await breaker.call(fail)
    with pytest.raises(ProviderTimeoutError):
        await breaker.call(fail)
    assert breaker.state == CircuitState.OPEN

    with pytest.raises(CircuitBreakerOpenError):
        await breaker.call(lambda: _success("blocked"))

    breaker.opened_at = datetime.now(UTC) - timedelta(seconds=61)
    assert await breaker.call(lambda: _success("ok")) == "ok"
    assert str(breaker.state) == "closed"
    assert breaker.failure_count == 0


@pytest.mark.asyncio
async def test_token_budget_ceiling_refuses_further_calls() -> None:
    """Exceeded token budgets trip and block later calls."""
    budget = TokenBudgetManager(
        default_run_token_limit=50,
        default_user_token_limit=50,
        default_run_cost_limit_usd=10,
        default_user_cost_limit_usd=10,
    )
    provider = MockProvider(ProviderName.GROQ, [response(ProviderName.GROQ, tokens=60)])
    client = fallback_client([provider], budget=budget)

    with pytest.raises(TokenBudgetExceededError):
        await client.generate(request(max_tokens=50))
    with pytest.raises(TokenBudgetExceededError):
        await client.generate(request(max_tokens=1))


def test_factory_selects_active_provider_from_settings() -> None:
    """AI_PROVIDER selects the concrete provider without code changes."""
    config = Settings(ai_provider="gemini", google_api_key="test-key")
    provider = create_provider(config)
    assert provider.name == ProviderName.GEMINI

    config_ollama = Settings(ai_provider="ollama")
    provider_ollama = create_provider(config_ollama)
    assert provider_ollama.name == ProviderName.OLLAMA


def test_fallback_chain_order_starts_with_gemini() -> None:
    """Fallback chain order is Gemini -> OpenAI -> Groq -> Ollama."""
    from app.ai.factory import create_fallback_provider

    fallback = create_fallback_provider(
        Settings(google_api_key="gemini-key", openai_api_keys=["openai-key"])
    )
    names = [p.name for p in fallback.providers]
    assert names == [
        ProviderName.GEMINI,
        ProviderName.OPENAI,
        ProviderName.ANTHROPIC,
        ProviderName.GROQ,
        ProviderName.OPENROUTER,
        ProviderName.OLLAMA,
    ]


async def _success(value: str) -> str:
    """Return a successful value for circuit breaker tests."""
    return value

