from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from app.core.sanitizer import sanitize_dict


class AuditLogRecord(BaseModel):
    """Structured audit record for state-changing operations."""

    log_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    user_id: str
    run_id: str | None = None
    agent_name: str | None = None
    action: str
    resource: str
    status: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class AuditLogger:
    """Append-only audit log manager for governance and compliance."""

    def __init__(self) -> None:
        self.records: list[AuditLogRecord] = []

    def log(
        self,
        user_id: str,
        action: str,
        resource: str,
        status: str = "success",
        run_id: str | None = None,
        agent_name: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AuditLogRecord:
        """Create and store a sanitized audit record."""
        clean_metadata = sanitize_dict(metadata or {})
        record = AuditLogRecord(
            log_id=f"audit-{len(self.records) + 1}",
            user_id=user_id,
            action=action,
            resource=resource,
            status=status,
            run_id=run_id,
            agent_name=agent_name,
            metadata=clean_metadata,
        )
        self.records.append(record)
        return record


audit_logger = AuditLogger()
