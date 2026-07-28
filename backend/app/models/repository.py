from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.run import Run


class Repository(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Connected GitHub repository."""

    __tablename__ = "repositories"
    __table_args__ = (UniqueConstraint("github_repo_id"),)

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE")
    )
    github_repo_id: Mapped[str] = mapped_column(String(64), index=True)
    owner: Mapped[str] = mapped_column(String(200), index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    default_branch: Mapped[str] = mapped_column(String(200), default="main")
    clone_url: Mapped[str] = mapped_column(String(1024))
    is_active: Mapped[bool] = mapped_column(default=True)

    organization: Mapped[Organization] = relationship(back_populates="repositories")
    runs: Mapped[list[Run]] = relationship(back_populates="repository")

