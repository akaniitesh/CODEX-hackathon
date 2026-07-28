from __future__ import annotations

from urllib.parse import urlencode

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.core.security import Role, create_access_token
from app.schemas.auth import GitHubUserProfile


class AuthService:
    """Authentication workflows for JWT and GitHub OAuth."""

    def __init__(self, session: AsyncSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings

    def build_github_authorization_url(self, state: str | None = None) -> str:
        """Build the GitHub OAuth authorization URL."""
        params = {
            "client_id": self.settings.github_client_id,
            "redirect_uri": str(self.settings.github_oauth_redirect_uri or ""),
            "scope": "read:user user:email",
        }
        if state:
            params["state"] = state
        return f"https://github.com/login/oauth/authorize?{urlencode(params)}"

    async def exchange_github_code(self, code: str) -> str:
        """Exchange a GitHub OAuth code for a platform JWT."""
        async with httpx.AsyncClient(timeout=10) as client:
            token_response = await client.post(
                "https://github.com/login/oauth/access_token",
                json={
                    "client_id": self.settings.github_client_id,
                    "client_secret": self.settings.github_client_secret,
                    "code": code,
                    "redirect_uri": str(self.settings.github_oauth_redirect_uri or ""),
                },
                headers={"Accept": "application/json"},
            )
            token_response.raise_for_status()
            access_token = token_response.json()["access_token"]
            profile = await self._fetch_github_profile(client, access_token)
        # User persistence is intentionally minimal until Phase 3 identity flows mature.
        return create_access_token(profile.github_user_id, Role.MEMBER, self.settings)

    async def _fetch_github_profile(
        self,
        client: httpx.AsyncClient,
        access_token: str,
    ) -> GitHubUserProfile:
        """Fetch and validate the authenticated GitHub profile."""
        response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        data = response.json()
        return GitHubUserProfile(
            github_user_id=str(data["id"]),
            login=data["login"],
            email=data.get("email"),
            avatar_url=data.get("avatar_url"),
        )

