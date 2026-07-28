from __future__ import annotations

from app.ai.http_provider import HttpChatProvider
from app.ai.keyring import ApiKeyRing
from app.ai.schemas import ProviderName


class GeminiProvider(HttpChatProvider):
    """Google Gemini OpenAI-compatible chat completions provider."""

    def __init__(
        self,
        api_keys: list[str],
        model: str,
        base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai",
    ) -> None:
        super().__init__(
            name=ProviderName.GEMINI,
            base_url=base_url,
            default_model=model,
            keyring=ApiKeyRing(api_keys),
        )


class OpenAIProvider(HttpChatProvider):
    """OpenAI chat completions provider."""

    def __init__(
        self,
        api_keys: list[str],
        model: str,
        base_url: str = "https://api.openai.com/v1",
    ) -> None:
        super().__init__(
            name=ProviderName.OPENAI,
            base_url=base_url,
            default_model=model,
            keyring=ApiKeyRing(api_keys),
        )


class GroqProvider(HttpChatProvider):
    """Groq OpenAI-compatible chat completions provider."""

    def __init__(
        self,
        api_keys: list[str],
        model: str,
        base_url: str = "https://api.groq.com/openai/v1",
    ) -> None:
        super().__init__(
            name=ProviderName.GROQ,
            base_url=base_url,
            default_model=model,
            keyring=ApiKeyRing(api_keys),
        )


class OllamaProvider(HttpChatProvider):
    """Local Ollama OpenAI-compatible chat provider."""

    def __init__(
        self,
        model: str,
        base_url: str = "http://localhost:11434/v1",
    ) -> None:
        super().__init__(
            name=ProviderName.OLLAMA,
            base_url=base_url,
            default_model=model,
            keyring=ApiKeyRing([]),
        )

