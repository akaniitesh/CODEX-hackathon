from __future__ import annotations

from functools import lru_cache

from pydantic import AliasChoices, AnyUrl, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    app_name: str = "Autonomous Software Engineering Platform"
    api_v1_prefix: str = "/api/v1"
    environment: str = Field(
        default="development",
        validation_alias=AliasChoices("ENVIRONMENT", "ENV", "environment"),
    )
    database_url: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/autose"
    )
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret_key: str = Field(
        default="dev-only-change-me",
        min_length=16,
        validation_alias=AliasChoices(
            "JWT_SECRET_KEY",
            "SECRET_KEY",
            "jwt_secret_key",
        ),
    )
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    github_client_id: str = ""
    github_client_secret: str = ""
    github_oauth_redirect_uri: AnyUrl | None = None
    github_webhook_secret: str = Field(
        default="",
        validation_alias=AliasChoices(
            "GITHUB_WEBHOOK_SECRET",
            "WEBHOOK_SECRET",
            "github_webhook_secret",
        ),
    )
    cors_origins: list[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    analysis_cache_ttl_seconds: int = 86_400
    ai_provider: str = "gemini"
    google_api_key: str = ""
    model_name: str = "gemini-1.5-flash"
    gemini_api_keys: list[str] = []
    gemini_model: str = "gemini-1.5-flash"
    gemini_base_url: str = (
        "https://generativelanguage.googleapis.com/v1beta/openai"
    )
    openai_api_keys: list[str] = []
    openai_model: str = "gpt-4.1-mini"
    openai_base_url: str = "https://api.openai.com/v1"
    groq_api_keys: list[str] = []
    groq_model: str = "llama-3.1-70b-versatile"
    groq_base_url: str = "https://api.groq.com/openai/v1"
    ollama_model: str = "llama3.1"
    ollama_base_url: str = "http://localhost:11434/v1"
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
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        """Parse comma-separated CORS origins from environment variables."""
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @field_validator(
        "openai_api_keys", "groq_api_keys", "gemini_api_keys", mode="before"
    )
    @classmethod
    def parse_api_keys(cls, value: str | list[str]) -> list[str]:
        """Parse comma-separated API keys for rotation."""
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @model_validator(mode="after")
    def validate_production_security(self) -> Settings:
        """Reject insecure defaults when running in production."""
        if self.environment.lower() != "production":
            return self
        if (
            self.jwt_secret_key == "dev-only-change-me"  # nosec B105
            or len(self.jwt_secret_key) < 32
        ):
            raise ValueError("JWT_SECRET_KEY must be configured for production.")
        if not self.github_webhook_secret:
            raise ValueError("GITHUB_WEBHOOK_SECRET must be configured for production.")
        if "*" in self.cors_origins:
            raise ValueError("Wildcard CORS origins are not allowed in production.")
        return self


@lru_cache
def get_settings() -> Settings:
    """Return cached settings for dependency injection."""
    return Settings()


settings = get_settings()
