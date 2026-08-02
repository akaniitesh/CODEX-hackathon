from __future__ import annotations

from app.ai.base import BaseAIProvider
from app.ai.budget import TokenBudgetManager
from app.ai.circuit_breaker import CircuitBreaker
from app.ai.fallback import FallbackAIProvider
from app.ai.providers import (
    AnthropicProvider,
    GeminiProvider,
    GroqProvider,
    OllamaProvider,
    OpenAIProvider,
    OpenRouterProvider,
)
from app.ai.retry import RetryPolicy
from app.ai.retry_queue import InMemoryRetryQueue
from app.ai.schemas import ProviderName
from app.core.config import Settings, settings


def create_provider(config: Settings = settings) -> BaseAIProvider:
    """Create the active provider selected by AI_PROVIDER."""
    provider_name = ProviderName(config.ai_provider.lower())
    providers = _provider_map(config)
    return providers[provider_name]


def create_fallback_provider(
    config: Settings = settings,
    retry_queue: InMemoryRetryQueue | None = None,
    budget_manager: TokenBudgetManager | None = None,
) -> FallbackAIProvider:
    """Create resilient provider chain:
    Gemini -> OpenAI -> Anthropic -> Groq -> OpenRouter -> Ollama.
    """
    providers = _provider_map(config)
    ordered = [
        providers[ProviderName.GEMINI],
        providers[ProviderName.OPENAI],
        providers[ProviderName.ANTHROPIC],
        providers[ProviderName.GROQ],
        providers[ProviderName.OPENROUTER],
        providers[ProviderName.OLLAMA],
    ]
    breakers = {
        provider.name: CircuitBreaker(
            provider=provider.name,
            failure_threshold=config.ai_circuit_failure_threshold,
            cooldown_seconds=config.ai_circuit_cooldown_seconds,
        )
        for provider in ordered
    }
    return FallbackAIProvider(
        providers=ordered,
        breakers=breakers,
        retry_policy=RetryPolicy(
            max_attempts=config.ai_retry_max_attempts,
            base_delay_seconds=config.ai_retry_base_delay_seconds,
        ),
        retry_queue=retry_queue or InMemoryRetryQueue(),
        budget_manager=budget_manager
        or TokenBudgetManager(
            default_run_token_limit=config.ai_run_token_limit,
            default_user_token_limit=config.ai_user_token_limit,
            default_run_cost_limit_usd=config.ai_run_cost_limit_usd,
            default_user_cost_limit_usd=config.ai_user_cost_limit_usd,
        ),
    )


def _provider_map(config: Settings) -> dict[ProviderName, BaseAIProvider]:
    """Build all configured concrete providers."""
    gemini_keys = config.gemini_api_keys or (
        [config.google_api_key] if config.google_api_key else []
    )
    gemini_model = config.gemini_model or config.model_name
    anthropic_keys = config.anthropic_api_keys or (
        [config.anthropic_api_key] if config.anthropic_api_key else []
    )
    openrouter_keys = config.openrouter_api_keys or (
        [config.openrouter_api_key] if config.openrouter_api_key else []
    )
    return {
        ProviderName.GEMINI: GeminiProvider(
            api_keys=gemini_keys,
            model=gemini_model,
            base_url=config.gemini_base_url,
        ),
        ProviderName.GROQ: GroqProvider(
            api_keys=config.groq_api_keys,
            model=config.groq_model,
            base_url=config.groq_base_url,
        ),
        ProviderName.OPENAI: OpenAIProvider(
            api_keys=config.openai_api_keys,
            model=config.openai_model,
            base_url=config.openai_base_url,
        ),
        ProviderName.ANTHROPIC: AnthropicProvider(
            api_keys=anthropic_keys,
            model=config.anthropic_model,
            base_url=config.anthropic_base_url,
        ),
        ProviderName.OPENROUTER: OpenRouterProvider(
            api_keys=openrouter_keys,
            model=config.openrouter_model,
            base_url=config.openrouter_base_url,
        ),
        ProviderName.OLLAMA: OllamaProvider(
            model=config.ollama_model,
            base_url=config.ollama_base_url,
        ),
    }


__all__ = ["create_provider", "create_fallback_provider"]
