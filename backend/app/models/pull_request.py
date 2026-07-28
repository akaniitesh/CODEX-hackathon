from __future__ import annotations

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class PullRequest(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Pull request opened or proposed by the platform."""

    __tablename__ = "pull_requests"

    run_id: Mapped[str] = mapped_column(ForeignKey("runs.id", ondelete="CASCADE"))
    github_pr_number: Mapped[int | None] = mapped_column(index=True)
    title: Mapped[str] = mapped_column(String(300))
    body: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), default="draft")
    url: Mapped[str | None] = mapped_column(String(1024))

