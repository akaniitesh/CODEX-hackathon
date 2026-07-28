from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any, TypeVar

import httpx
from pydantic import BaseModel, ValidationError

from app.ai.base import BaseAIProvider
from app.ai.errors import (
    ProviderNetworkError,
    ProviderResponseError,
    ProviderServerError,
    ProviderTimeoutError,
    RateLimitError,
    TerminalAIProviderError,
)
from app.ai.keyring import ApiKeyRing
from app.ai.schemas import (
    AIRequest,
    AIResponse,
    ProviderName,
    StreamChunk,
    TokenUsage,
)

StructuredT = TypeVar("StructuredT", bound=BaseModel)


class HttpChatProvider(BaseAIProvider):
    """Base HTTP chat provider for OpenAI-compatible APIs."""

    def __init__(
        self,
        name: ProviderName,
        base_url: str,
        default_model: str,
        keyring: ApiKeyRing | None = None,
        timeout_seconds: float = 30.0,
    ) -> None:
        self.name = name
        self.base_url = base_url.rstrip("/")
        self.default_model = default_model
        self.keyring = keyring or ApiKeyRing([])
        self.timeout_seconds = timeout_seconds

    async def generate(self, request: AIRequest) -> AIResponse:
        """Generate a complete model response."""
        payload = self._build_payload(request, stream=False)
        data = await self._post_json(payload)
        return self._parse_response(data, request.model or self.default_model)

    async def stream(self, request: AIRequest) -> AsyncIterator[StreamChunk]:
        """Stream model response chunks."""
        payload = self._build_payload(request, stream=True)
        headers = self._headers()
        try:
            async with (
                httpx.AsyncClient(timeout=self.timeout_seconds) as client,
                client.stream(
                    "POST",
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers,
                ) as response,
            ):
                self._raise_for_status(response.status_code)
                async for line in response.aiter_lines():
                    chunk = self._parse_stream_line(
                        line,
                        request.model or self.default_model,
                    )
                    if chunk is not None:
                        yield chunk
        except httpx.TimeoutException as exc:
            raise ProviderTimeoutError(
                "Provider stream timed out.", self.name
            ) from exc
        except httpx.RequestError as exc:
            raise ProviderNetworkError(
                "Provider stream network error.", self.name
            ) from exc

    async def structured_output(
        self,
        request: AIRequest,
        schema: type[StructuredT],
    ) -> StructuredT:
        """Generate and validate a structured response without guessing fields."""
        response = await self.generate(request)
        try:
            return schema.model_validate_json(response.content)
        except ValidationError as exc:
            raise ProviderResponseError(
                "Provider returned malformed structured output.",
                self.name,
            ) from exc

    def _build_payload(self, request: AIRequest, stream: bool) -> dict[str, Any]:
        """Build an OpenAI-compatible chat payload."""
        return {
            "model": request.model or self.default_model,
            "messages": [message.model_dump() for message in request.messages],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": stream,
        }

    async def _post_json(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Send a JSON request and map HTTP errors to provider errors."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=self._headers(),
                )
        except httpx.TimeoutException as exc:
            raise ProviderTimeoutError(
                "Provider request timed out.", self.name
            ) from exc
        except httpx.RequestError as exc:
            raise ProviderNetworkError(
                "Provider network error.", self.name
            ) from exc
        data = response.json()
        if not isinstance(data, dict):
            raise ProviderResponseError("Provider response is not a dict.", self.name)
        return data

    def _headers(self) -> dict[str, str]:
        """Build request headers with the next rotated key."""
        headers = {"Content-Type": "application/json"}
        api_key = self.keyring.next_key()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        return headers

    def _raise_for_status(self, status_code: int) -> None:
        """Map provider status codes to retryable or terminal errors."""
        if status_code < 400:
            return
        if status_code == 429:
            raise RateLimitError("Provider rate limit exceeded.", self.name)
        if 500 <= status_code <= 599:
            raise ProviderServerError("Provider server error.", self.name)
        raise TerminalAIProviderError(
            f"Provider terminal HTTP error: {status_code}.",
            self.name,
        )

    def _parse_response(self, data: dict[str, Any], model: str) -> AIResponse:
        """Parse an OpenAI-compatible chat completion response."""
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderResponseError(
                "Provider response shape is invalid.", self.name
            ) from exc
        usage_data = data.get("usage") or {}
        total = int(usage_data.get("total_tokens") or 0)
        usage = TokenUsage(
            prompt_tokens=int(usage_data.get("prompt_tokens") or 0),
            completion_tokens=int(usage_data.get("completion_tokens") or 0),
            total_tokens=total,
            estimated_cost_usd=0.0,
        )
        return AIResponse(
            provider=self.name, model=model, content=str(content), usage=usage
        )

    def _parse_stream_line(self, line: str, model: str) -> StreamChunk | None:
        """Parse one server-sent event line."""
        if not line.startswith("data: "):
            return None
        raw = line.removeprefix("data: ").strip()
        if raw == "[DONE]":
            return StreamChunk(provider=self.name, model=model, delta="", done=True)
        try:
            data = json.loads(raw)
            delta = data["choices"][0].get("delta", {}).get("content", "")
        except (json.JSONDecodeError, KeyError, IndexError, TypeError):
            return None
        return StreamChunk(provider=self.name, model=model, delta=str(delta))
