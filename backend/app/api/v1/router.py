from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints import metrics
from app.api.v1.routers import auth, health, repositories, runs, webhooks, ws

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(metrics.router, tags=["telemetry"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(
    repositories.router, prefix="/repositories", tags=["repositories"]
)
api_router.include_router(runs.router, prefix="/runs", tags=["runs"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
api_router.include_router(ws.router, prefix="/ws", tags=["websocket"])

