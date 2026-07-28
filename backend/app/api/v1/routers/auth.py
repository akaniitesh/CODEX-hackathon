from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.dependencies import get_auth_service
from app.schemas.auth import (
    GitHubOAuthCallbackRequest,
    GitHubOAuthStartResponse,
    TokenResponse,
)
from app.services.auth_service import AuthService

router = APIRouter()


@router.get("/github/start", response_model=GitHubOAuthStartResponse)
async def github_oauth_start(
    state: str | None = None,
    service: AuthService = Depends(get_auth_service),
) -> GitHubOAuthStartResponse:
    """Return the GitHub OAuth authorization URL."""
    return GitHubOAuthStartResponse(
        authorization_url=service.build_github_authorization_url(state)
    )


@router.post("/github/callback", response_model=TokenResponse)
async def github_oauth_callback(
    payload: GitHubOAuthCallbackRequest,
    service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """Exchange a GitHub OAuth callback code for a JWT."""
    token = await service.exchange_github_code(payload.code)
    return TokenResponse(access_token=token)

