from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.execution import Execution
    from app.models.repository import Repository
    from app.models.timeline_event import TimelineEvent


class Run(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Top-level autonomous run triggered by a user or webhook."""

    __tablename__ = "runs"
    __table_args__ = (
        UniqueConstraint("repository_id", "commit_sha", "event_type"),
        UniqueConstraint("webhook_delivery_id"),
    )

    repository_id: Mapped[str] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        index=True,
    )
    event_type: Mapped[str] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(40), default="queued", index=True)
    commit_sha: Mapped[str] = mapped_column(String(64), index=True)
    branch: Mapped[str | None] = mapped_column(String(200))
    webhook_delivery_id: Mapped[str | None] = mapped_column(String(128), index=True)
    plan_summary: Mapped[str | None] = mapped_column(Text)

    repository: Mapped[Repository] = relationship(back_populates="runs")
    executions: Mapped[list[Execution]] = relationship(back_populates="run")
    events: Mapped[list[TimelineEvent]] = relationship(back_populates="run")

