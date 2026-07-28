from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, HttpUrl


class RepositoryRead(BaseModel):
    """API representation of a connected repository."""

    id: str
    github_repo_id: str
    owner: str
    name: str
    default_branch: str
    clone_url: HttpUrl
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

