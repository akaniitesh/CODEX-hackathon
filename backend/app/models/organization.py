from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.membership import Membership
    from app.models.repository import Repository


class Organization(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Tenant-like workspace for v1 RBAC without full multitenancy hardening."""

    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(200))
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)

    memberships: Mapped[list[Membership]] = relationship(back_populates="organization")
    repositories: Mapped[list[Repository]] = relationship(back_populates="organization")

