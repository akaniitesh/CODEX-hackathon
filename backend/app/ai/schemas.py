from __future__ import annotations

from collections.abc import AsyncIterator
from enum import StrEnum

from pydantic import BaseModel, Field


class ProviderName(StrEnum):
    """Supported AI providers."""

    GEMINI = "gemini"
    GROQ = "groq"
    OPENAI = "openai"
    OLLAMA = "ollama"
    ANTHROPIC = "anthropic"
    OPENROUTER = "openrouter"


class AIMessage(BaseModel):
    """Chat message sent to a model provider."""

    role: str = Field(pattern="^(system|user|assistant|tool)$")
    content: str = Field(min_length=1)


class AIRequest(BaseModel):
    """Provider-agnostic generation request."""

    messages: list[AIMessage]
    model: str | None = None
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1_024, ge=1, le=128_000)
    run_id: str | None = None
    user_id: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)


class TokenUsage(BaseModel):
    """Token usage and estimated cost reported by a provider call."""

    prompt_tokens: int = Field(default=0, ge=0)
    completion_tokens: int = Field(default=0, ge=0)
    total_tokens: int = Field(default=0, ge=0)
    estimated_cost_usd: float = Field(default=0.0, ge=0.0)


class AIResponse(BaseModel):
    """Provider-agnostic generation response."""

    provider: ProviderName
    model: str
    content: str
    usage: TokenUsage = Field(default_factory=TokenUsage)


class StreamChunk(BaseModel):
    """Provider-agnostic streaming response chunk."""

    provider: ProviderName
    model: str
    delta: str
    done: bool = False


StructuredModel = type[BaseModel]
StreamResult = AsyncIterator[StreamChunk]

__all__ = [
    "ProviderName",
    "AIMessage",
    "AIRequest",
    "TokenUsage",
    "AIResponse",
    "StreamChunk",
    "StructuredModel",
    "StreamResult",
]
