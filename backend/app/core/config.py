from __future__ import annotations

from functools import lru_cache

from pydantic import AliasChoices, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application configuration using Pydantic Settings."""

    app_name: str = "Aegis AI"
    project_name: str = "Aegis AI"
    environment: str = "development"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    analysis_cache_ttl_seconds: int = 3600

    # Database & Cache Settings
    database_url: str = "postgresql+asyncpg://autose_user:autose_password@localhost:5432/autose_platform"
    redis_url: str = "redis://localhost:6379/0"

    # JWT & Webhook Security
    jwt_secret_key: str = Field(
        default="ca18ff6130fbbeaa168594fcec60ecff9109b7f3b4978ff2406f283b573c8c44",
        validation_alias=AliasChoices("jwt_secret_key", "secret_key"),
    )
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    jwt_expire_minutes: int = 60
    github_webhook_secret: str = Field(
        default="change-this-to-a-secure-webhook-secret",
        validation_alias=AliasChoices("github_webhook_secret", "webhook_secret"),
    )
    cors_origins: list[str] = ["http://localhost", "http://localhost:3000", "http://127.0.0.1:3000"]

    # GitHub OAuth App Credentials
    github_client_id: str = "your-github-client-id"
    github_client_secret: str = "your-github-client-secret"
    github_oauth_redirect_uri: str = "http://localhost:3000/auth/github/callback"

    # AI Provider API Keys & Configuration
    ai_provider: str = "gemini"
    google_api_key: str = ""
    model_name: str = "gemini-3.5-flash"
    gemini_api_keys: list[str] = []
    gemini_model: str = "gemini-3.5-flash"
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai"

    openai_api_key: str = ""
    openai_api_keys: list[str] = []
    openai_model: str = "gpt-4.1-mini"
    openai_base_url: str = "https://api.openai.com/v1"

    groq_api_key: str = ""
    groq_api_keys: list[str] = []
    groq_model: str = "llama-3.1-70b-versatile"
    groq_base_url: str = "https://api.groq.com/openai/v1"

    anthropic_api_key: str = ""
    anthropic_api_keys: list[str] = []
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    anthropic_base_url: str = "https://api.anthropic.com/v1"

    openrouter_api_key: str = ""
    openrouter_api_keys: list[str] = []
    openrouter_model: str = "anthropic/claude-3.5-sonnet"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    ollama_model: str = "llama3.1"
    ollama_base_url: str = "http://localhost:11434/v1"

    # Circuit Breaker & Budget Guardrails
    ai_circuit_failure_threshold: int = 3
    ai_circuit_cooldown_seconds: float = 30.0
    ai_retry_max_attempts: int = 3
    ai_retry_base_delay_seconds: float = 0.25
    ai_user_token_limit: int = 200_000
    ai_run_token_limit: int = 100_000
    ai_user_cost_limit_usd: float = 25.0
    ai_run_cost_limit_usd: float = 10.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        populate_by_name=True,
        extra="ignore",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        """Parse comma-separated CORS origins from environment variables."""
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @field_validator(
        "openai_api_keys",
        "groq_api_keys",
        "gemini_api_keys",
        "anthropic_api_keys",
        "openrouter_api_keys",
        mode="before",
    )
    @classmethod
    def parse_api_keys(cls, value: str | list[str]) -> list[str]:
        """Parse comma-separated API keys for rotation."""
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @model_validator(mode="after")
    def initialize_api_keys(self) -> Settings:
        """Initialize plural api key lists from singular variables if empty."""
        if not self.openai_api_keys and self.openai_api_key:
            self.openai_api_keys = [
                item.strip()
                for item in self.openai_api_key.split(",")
                if item.strip()
            ]
        if not self.groq_api_keys and self.groq_api_key:
            self.groq_api_keys = [
                item.strip()
                for item in self.groq_api_key.split(",")
                if item.strip()
            ]
        if not self.gemini_api_keys and self.google_api_key:
            self.gemini_api_keys = [
                item.strip()
                for item in self.google_api_key.split(",")
                if item.strip()
            ]
        if not self.anthropic_api_keys and self.anthropic_api_key:
            self.anthropic_api_keys = [
                item.strip()
                for item in self.anthropic_api_key.split(",")
                if item.strip()
            ]
        if not self.openrouter_api_keys and self.openrouter_api_key:
            self.openrouter_api_keys = [
                item.strip()
                for item in self.openrouter_api_key.split(",")
                if item.strip()
            ]
        if self.environment.lower() in ("production", "prod"):
            insecure_defaults = (
                "dev-only-change-me",
                "ca18ff6130fbbeaa168594fcec60ecff9109b7f3b4978ff2406f283b573c8c44",
                "change-this-to-a-secure-webhook-secret",
            )
            if self.jwt_secret_key in insecure_defaults:
                msg = (
                    "JWT_SECRET_KEY must be configured securely "
                    "in production environment."
                )
                raise ValueError(msg)
        return self


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton factory."""
    return Settings()


settings: Settings = get_settings()

__all__ = ["Settings", "get_settings", "settings"]
