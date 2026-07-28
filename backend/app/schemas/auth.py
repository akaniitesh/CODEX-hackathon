from __future__ import annotations

from pydantic import BaseModel, HttpUrl


class GitHubOAuthStartResponse(BaseModel):
    """URL used to begin GitHub OAuth."""

    authorization_url: str


class GitHubOAuthCallbackRequest(BaseModel):
    """GitHub OAuth callback payload."""

    code: str
    state: str | None = None


class TokenResponse(BaseModel):
    """JWT response returned after successful authentication."""

    access_token: str
    token_type: str = "bearer"


class GitHubUserProfile(BaseModel):
    """Validated subset of a GitHub user profile."""

    github_user_id: str
    login: str
    email: str | None = None
    avatar_url: HttpUrl | None = None

