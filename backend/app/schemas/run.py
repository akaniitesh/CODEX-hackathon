from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class RunRead(BaseModel):
    """API representation of a run."""

    id: str
    repository_id: str
    event_type: str
    status: str
    commit_sha: str
    branch: str | None
    webhook_delivery_id: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

