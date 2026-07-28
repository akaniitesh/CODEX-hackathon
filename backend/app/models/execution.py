from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.run import Run


class Execution(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Individual agent/tool execution record inside a run."""

    __tablename__ = "executions"

    run_id: Mapped[str] = mapped_column(ForeignKey("runs.id", ondelete="CASCADE"))
    agent_name: Mapped[str] = mapped_column(String(120), index=True)
    status: Mapped[str] = mapped_column(String(40), default="queued", index=True)
    webhook_delivery_id: Mapped[str | None] = mapped_column(String(128), index=True)
    input_summary: Mapped[str | None] = mapped_column(Text)
    output_summary: Mapped[str | None] = mapped_column(Text)
    error_message: Mapped[str | None] = mapped_column(Text)

    run: Mapped[Run] = relationship(back_populates="executions")

