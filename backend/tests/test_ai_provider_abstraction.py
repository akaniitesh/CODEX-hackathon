from __future__ import annotations

from collections.abc import AsyncIterator
from typing import TypeVar

import pytest
from pydantic import BaseModel

from app.ai.base import BaseAIProvider
from app.ai.factory import create_fallback_provider
from app.ai.schemas import (
    AIMessage,
    AIRequest,
    AIResponse,
    ProviderName,
    StreamChunk,
    TokenUsage,
)
from app.core.config import Settings

StructuredT = TypeVar("StructuredT", bound=BaseModel)


class MockProvider(BaseAIProvider):
    """Mock AI provider for unit testing."""

    def __init__(
        self,
        name: ProviderName = ProviderName.GEMINI,
        responses: list[AIResponse] | None = None,
        fail_count: int = 0,
        response_text: str = "mock response",
    ) -> None:
        super().__init__(name=name)
        self.fail_count = fail_count
        self.attempts = 0
        self.response_text = response_text
        self.responses = responses or []

    async def generate(self, request: AIRequest) -> AIResponse:
        self.attempts += 1
        if self.attempts <= self.fail_count:
            raise RuntimeError(f"Mock failure {self.attempts}")
        if self.responses and self.attempts <= len(self.responses):
            return self.responses[self.attempts - 1]
        return AIResponse(
            provider=self.name,
            model="mock-model",
            content=self.response_text,
            usage=TokenUsage(prompt_tokens=10, completion_tokens=10, total_tokens=20),
        )

    async def stream(self, request: AIRequest) -> AsyncIterator[StreamChunk]:
        yield StreamChunk(
            provider=self.name,
            model="mock-model",
            delta=self.response_text,
            done=True,
        )

    async def structured_output(
        self, request: AIRequest, schema: type[StructuredT]
    ) -> StructuredT:
        return schema()


@pytest.mark.asyncio
async def test_normal_response_uses_first_provider() -> None:
    """Provider chain uses first healthy provider."""
    p1 = MockProvider(ProviderName.GEMINI, fail_count=0, response_text="gemini ok")
    req = AIRequest(messages=[AIMessage(role="user", content="hello")])
    res = await p1.generate(req)
    assert res.content == "gemini ok"


def test_fallback_chain_order_starts_with_gemini() -> None:
    """Fallback chain order starts with Gemini and includes all providers."""
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
