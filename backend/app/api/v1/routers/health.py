from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    """Return process health."""
    return {"status": "ok"}


@router.get("/health/db")
async def database_health(
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, str]:
    """Return database connectivity health."""
    await session.execute(text("SELECT 1"))
    return {"status": "ok"}

