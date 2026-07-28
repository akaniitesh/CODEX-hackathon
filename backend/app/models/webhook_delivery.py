from __future__ import annotations

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class WebhookDelivery(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Idempotency ledger for GitHub webhook deliveries."""

    __tablename__ = "webhook_deliveries"

    delivery_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    event_type: Mapped[str] = mapped_column(String(80), index=True)
    repository_full_name: Mapped[str | None] = mapped_column(String(420), index=True)
    commit_sha: Mapped[str | None] = mapped_column(String(64), index=True)
    status: Mapped[str] = mapped_column(String(40), default="received")
    payload_summary: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)

