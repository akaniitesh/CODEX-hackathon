from __future__ import annotations

from pydantic import BaseModel, Field


class GitHubWebhookSummary(BaseModel):
    """Trusted summary extracted from a GitHub webhook payload."""

    delivery_id: str = Field(min_length=1, max_length=128)
    event_type: str = Field(min_length=1, max_length=80)
    repository_full_name: str | None = Field(default=None, max_length=420)
    commit_sha: str | None = Field(default=None, max_length=64)
    branch: str | None = Field(default=None, max_length=200)


class WebhookAcceptedResponse(BaseModel):
    """Webhook processing result."""

    accepted: bool
    duplicate: bool
    run_id: str | None = None

