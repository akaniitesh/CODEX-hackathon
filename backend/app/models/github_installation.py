from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class GitHubInstallation(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """GitHub App installation linked to an organization."""

    __tablename__ = "github_installations"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE")
    )
    github_installation_id: Mapped[str] = mapped_column(String(64), unique=True)
    account_login: Mapped[str] = mapped_column(String(200), index=True)
    account_type: Mapped[str] = mapped_column(String(32))

